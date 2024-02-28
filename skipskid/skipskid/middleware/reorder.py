from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve, Resolver404

from copy import deepcopy
from six import string_types

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class ModelAdminReorder(MiddlewareMixin):

    def init_config(self, request, available_apps):
        self.request = request
        self.available_apps = available_apps

        self.config = getattr(settings, 'ADMIN_REORDER', None)
        if not self.config:
            # ADMIN_REORDER settings is not defined.
            raise ImproperlyConfigured('ADMIN_REORDER config is not defined.')

        if not isinstance(self.config, (tuple, list)):
            raise ImproperlyConfigured(
                'ADMIN_REORDER config parameter must be tuple or list. '
                'Got {config}'.format(config=self.config))

        admin_index = admin.site.index(request)
        try:
            # try to get all installed models
            available_apps = admin_index.context_data['available_apps']
        except KeyError:
            # use available_apps from context if this fails
            pass

        # Flatten all models from apps
        self.models_list = []
        for app in available_apps:
            for model in app['models']:
                model['model_name'] = self.get_model_name(
                    app['app_label'], model['object_name'])
                self.models_list.append(model)

    def get_available_apps(self):
        ordered_available_apps = []
        for app_config in self.config:
            app = self.make_app(app_config)
            if app:
                ordered_available_apps.append(app)
        return ordered_available_apps

    def make_app(self, app_config):
        if not isinstance(app_config, (dict, string_types)):
            raise TypeError('ADMIN_REORDER list item must be '
                            'dict or string. Got %s' % repr(app_config))

        if isinstance(app_config, string_types):
            # Keep original label and models
            return self.find_app(app_config)
        else:
            return self.process_app(app_config)

    def find_app(self, app_label):
        for app in self.available_apps:
            if app['app_label'] == app_label:
                return app

    def get_model_name(self, app_name, model_name):
        if '.' not in model_name:
            model_name = '%s.%s' % (app_name, model_name)
        return model_name

    def process_app(self, app_config):
        if 'app' not in app_config:
            raise NameError('ADMIN_REORDER list item must define '
                            'a "app" name. Got %s' % repr(app_config))

        app = self.find_app(app_config['app'])
        if app:
            app = deepcopy(app)
            # Rename app
            if 'label' in app_config:
                app['name'] = app_config['label']

            # Process app models
            if 'models' in app_config:
                models_config = app_config.get('models')
                models = self.process_models(models_config)
                if models:
                    app['models'] = models
                else:
                    return None
            return app

    def process_models(self, models_config):
        if not isinstance(models_config, (dict, list, tuple)):
            raise TypeError('"models" config for ADMIN_REORDER list '
                            'item must be dict or list/tuple. '
                            'Got %s' % repr(models_config))

        ordered_models_list = []
        for model_config in models_config:
            model = None
            if isinstance(model_config, dict):
                model = self.process_model(model_config)
            else:
                model = self.find_model(model_config)

            if model:
                ordered_models_list.append(model)

        return ordered_models_list

    def find_model(self, model_name):
        for model in self.models_list:
            if model['model_name'] == model_name:
                return model

    def process_model(self, model_config):
        # Process model defined as { model: 'model', 'label': 'label' }
        for key in ('model', 'label', ):
            if key not in model_config:
                return
        model = self.find_model(model_config['model'])
        if model:
            model['name'] = model_config['label']
            return model

    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            return response
        if not url.app_name == 'admin' and \
                url.url_name not in ['index', 'available_apps']:
            # current view is not a django admin index
            # or available_apps view, bail out!
            return response

        try:
            available_apps = response.context_data['available_apps']
        except KeyError:
            # there is no available_apps! nothing to reorder
            return response

        self.init_config(request, available_apps)
        ordered_available_apps = self.get_available_apps()
        response.context_data['available_apps'] = ordered_available_apps
        response.context_data['available_apps'] = ordered_available_apps

        return response
