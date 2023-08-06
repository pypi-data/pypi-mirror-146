
asset_list = {}


class asset_enroller(object):
    def __init__(self, cls, *args, **kwargs):
        asset_list.update({
            cls.__name__: cls
        })

        self.cls = cls

    def __call__(self, *args, **kwargs):
        pass

# def asset_enroller(module):
#     """
#     register the commands which are hooked up with this decorator,
#     commandline tool can directly execute the command for getting something fun

#     Arguments:
#         module {string} -- represent the module name of command

#     Keyword Arguments:
#         scope {int} -- represent the scope for access controlling
#                        (default: {0} means it can be accessed by all users)
#         alias {string} -- represent another short name for the key of command dict
#                           (default: {None})
#         debug {bool} -- represent the flag for debugging commands

#         response_type {ResponseType} -- Represent the response result types.

#         singleton {bool} -- Represent the task queue mode, singleton: only allow a
#         single job at the same time when having multi-threads mode
#     """

#     class Decorator(object):
#         """
#         Decorator for registering commands
#         """

#         def __init__(self, fn):
#             self.fn = fn
#             asset_model_name = fn.__qualname__
#             print(asset_model_name)
#             # if cmd_str not in asset_list:
#             #     command_list[alias if alias else cmd_str] = {
#             #         'scopes': scopes,
#             #         'singleton': singleton,
#             #         'full_name': f"{module}.{fn.__qualname__}"}
#             # update_wrapper(self, fn)
#     return Decorator
