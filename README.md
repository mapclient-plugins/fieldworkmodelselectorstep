fieldworkmodelselectorstep
========================
MAP Client plugin for selecting a model by name from a dictionary of fieldwork models.

Requires
--------
None

Inputs
------
- **ju#fieldworkmodeldict** - A dictionary of model names (str) mapping to fieldwork model instances

Outputs
-------
- **ju#fieldworkmodel** - A fieldwork model instance from the input dictionary matching the configured name.

Configuration
-------------
- **identifier** : Unique name for the step.
- **Model Name** : The name key of the fieldwork model to be extracted from the input model dictionary.

Usage
-----
The configured model name must match one of the keys of the input dict.