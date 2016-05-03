Quick Start
===========


methods
-------

.. method:: get_model(model, pk=None, cache_exc=False, **kwargs)

    Return django model in cache, query database when cache miss hit, raise Model.DoesNotExist when miss database.

    Set cache_exc=True where cache model.DoesNotExist in cache, and return None.


.. method:: get_model_list(model, **kwargs)

    Get multiple models with filter on fields, return a list of models.

.. method:: clear_model(model, *args)

    clear model cache on args, usually use id.

.. method:: clear_model_list(model, *agrs)

    Clear model cache using field name.

.. method:: clear_model_cache(model, *agrs, **kwargs)

    Call clear_model or clear_model_list dynamically according to params passed.
