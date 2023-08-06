# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jax_metrics',
 'jax_metrics.losses',
 'jax_metrics.metrics',
 'jax_metrics.metrics.tm_port',
 'jax_metrics.metrics.tm_port.classification',
 'jax_metrics.metrics.tm_port.functional',
 'jax_metrics.metrics.tm_port.functional.classification',
 'jax_metrics.metrics.tm_port.utilities',
 'jax_metrics.regularizers']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'einops>=0.4.0,<0.5.0',
 'optax>=0.1.1,<0.2.0',
 'treeo>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'jax-metrics',
    'version': '0.1.0a0',
    'description': '',
    'long_description': '# JAX Metrics\n\n_A Metrics library for the JAX ecosystem_\n\n#### Main Features\n* Standard framework-independent metrics that can be used in any JAX project.\n* Pytree-based abstractions that can natively integrate with all JAX APIs.\n* Distributed-friendly APIs that make it super easy to synchronize metrics across devices.\n* Automatic accumulation over entire epochs.\n\n\nJAX Metrics is implemented on top of [Treeo](https://github.com/cgarciae/treeo).\n\n## What is included?\n* A Keras-like `Metric` abstraction.\n* A Keras-like `Loss` abstraction.\n* A `Metrics`, `Losses`, and `LossesAndMetrics` combinators.\n* A `metrics` moduel containing popular metrics.\n* A `losses` and `regularizers` module containing popular losses.\n\n<!-- ## Why JAX Metrics? -->\n\n## Installation\nInstall using pip:\n```bash\npip install jax_metrics\n```\n\n## Getting Started\n\n```python\nimport jax_metrics as jm\n\nmetric = jm.metrics.Accuracy()\n\n# Initialize the metric\nmetric = metric.reset()\n\n# Update the metric with a batch of predictions and labels\nmetric = metric.update(target=y, preds=logits)\n\n# Get the current value of the metric\nacc = metric.compute() # 0.95\n\n# alternatively, produce a logs dict\nlogs = metric.compute_logs() # {\'accuracy\': 0.95}\n```\n\n```python\nimport jax_metrics as jm\n\nmetric = jm.metrics.Accuracy()\n\n@jax.jit\ndef init_step(metric: jm.Metric) -> jm.Metric:\n    return metric.reset()\n\n\ndef loss_fn(params, metric, x, y):\n    ...\n    metric = metric.update(target=y, preds=logits)\n    ...\n\n    return loss, metric\n\n@jax.jit\ndef train_step(params, metric, x, y):\n    grads, metric = jax.grad(loss_fn, has_aux=True)(\n        params, metric, x, y\n    )\n    ...\n    return params, metric\n```\n\n```python\ndef loss_fn(params, metric, x, y):\n    ...\n    # compuate batch update\n    batch_updates = metric.batch_updates(target=y, preds=logits)\n    # gather over all devices and aggregate\n    batch_updates = jax.lax.all_gather(batch_updates, "device").aggregate()\n    # update metric\n    metric = metric.merge(batch_updates)\n    ...\n```\n\n```python\nbatch_updates = jax.lax.psum(batch_updates, "device")\n```\n\n```python\nmetrics = jm.Metrics([\n    jm.metrics.Accuracy(),\n    jm.metrics.F1(), # not yet implemented 😅, coming soon?\n])\n\n# same API\nmetrics = metrics.reset()\n# same API\nmetrics = metrics.update(target=y, preds=logits)\n# compute new returns a dict\nmetrics.compute() # {\'accuracy\': 0.95, \'f1\': 0.87}\n# same as compute_logs in the case\nmetrics.compute_logs() # {\'accuracy\': 0.95, \'f1\': 0.87}\n```\n\n```python\nmetrics = jm.Metrics({\n    "acc": jm.metrics.Accuracy(),\n    "f_one": jm.metrics.F1(), # not yet implemented 😅, coming soon?\n})\n\n# same API\nmetrics = metrics.reset()\n# same API\nmetrics = metrics.update(target=y, preds=logits)\n# compute new returns a dict\nmetrics.compute() # {\'acc\': 0.95, \'f_one\': 0.87}\n# same as compute_logs in the case\nmetrics.compute_logs() # {\'acc\': 0.95, \'f_one\': 0.87}\n```\n\n```python\nlosses = jm.Losses([\n    jm.losses.Crossentropy(),\n    jm.regularizers.L2(1e-4),\n])\n\n# same API\nlosses = losses.reset()\n# same API\nlosses = losses.update(target=y, preds=logits, parameters=params)\n# compute new returns a dict\nlosses.compute() # {\'crossentropy\': 0.23, \'l2\': 0.005}\n# same as compute_logs in the case\nlosses.compute_logs() # {\'crossentropy\': 0.23, \'l2\': 0.005}\n# you can also compute the total loss\ntotal_loss = losses.total_loss() # 0.235\n```\n\n```python\nlosses = jm.Losses({\n    "xent": jm.losses.Crossentropy(),\n    "l_two": jm.regularizers.L2(1e-4),\n})\n\n# same API\nlosses = losses.reset()\n# same API\nlosses = losses.update(target=y, preds=logits, parameters=params)\n# compute new returns a dict\nlosses.compute() # {\'xent\': 0.23, \'l_two\': 0.005}\n# same as compute_logs in the case\nlosses.compute_logs() # {\'xent\': 0.23, \'l_two\': 0.005}\n# you can also compute the total loss\ntotal_loss = losses.total_loss() # 0.235\n```\n\n```python\ndef loss_fn(...):\n    ...\n    batch_updates = losses.loss_and_update(target=y, preds=logits, parameters=params)\n    loss = batch_updates.total_loss()\n    losses = losses.merge(batch_updates)\n    ...\n    return loss, losses\n```\n\n```python\ndef loss_fn(...):\n    ...\n    loss, lossses = losses.loss_and_update(target=y, preds=logits, parameters=params)\n    ...\n    return loss, losses\n```\n\n```python\nlms = jm.LossesAndMetrics(\n    metrics=[\n        jm.metrics.Accuracy(),\n        jm.metrics.F1(), # not yet implemented 😅, coming soon?\n    ],\n    losses=[\n        jm.losses.Crossentropy(),\n        jm.regularizers.L2(1e-4),\n    ],\n)\n\n# same API\nlms = lms.reset()\n# same API\nlms = lms.update(target=y, preds=logits, parameters=params)\n# compute new returns a dict\nlms.compute() # {\'accuracy\': 0.95, \'f1\': 0.87, \'crossentropy\': 0.23, \'l2\': 0.005}\n# same as compute_logs in the case\nlms.compute_logs() # {\'accuracy\': 0.95, \'f1\': 0.87, \'crossentropy\': 0.23, \'l2\': 0.005}\n# you can also compute the total loss\ntotal_loss = lms.total_loss() # 0.235\n```\n\n```python\ndef loss_fn(...):\n    ...\n    batch_updates = lms.batch_updates(target=y, preds=logits, parameters=params)\n    loss = batch_updates.total_loss()\n    lms = lms.merge(batch_updates)\n    ...\n    return loss, lms\n```\n\n```python\ndef loss_fn(...):\n    ...\n    loss, lms = lms.loss_and_update(target=y, preds=logits, parameters=params)\n    ...\n    return loss, lms\n```\n\n```python\ndef loss_fn(...):\n    ...\n    batch_updates = lms.batch_updates(target=y, preds=logits, parameters=params)\n    loss = batch_updates.total_loss()\n    batch_updates = jax.lax.all_gather(batch_updates, "device").aggregate()\n    lms = lms.merge(batch_updates)\n    ...\n    return loss, lms\n```',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cgarciae.github.io/jax_metrics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
