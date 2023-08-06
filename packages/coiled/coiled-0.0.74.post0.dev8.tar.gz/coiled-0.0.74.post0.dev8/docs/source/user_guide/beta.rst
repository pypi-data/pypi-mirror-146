Beta
====

Coiled V2 beta is an early preview of our rewritten backend.

It was written with the following objectives:

-   **Reliability**: clusters come up with greater certainty, especially at larger scale.
-   **Cost**: we provide a richer and more responsive access to sets of instance types and spot instances.
-   **Visibility**: when situations occur, issues are more plainly visible and easier to debug.

V2 provides both a richer and more robust interaction with the underlying cloud,
and delivers this information to you so that you can understand what is going
on.

    .. figure:: images/widget.png
       :alt: Terminal dashboard displaying the Coiled cluster status overview, configuration, and Dask worker states.

Getting started
---------------

A few extra permissions are required if you are using Coiled in your own cloud provider account.

.. dropdown:: Extra AWS IAM Policy

    .. code-block::

        ec2:CreateFleet
        ec2:CreateLaunchTemplate
        ec2:CreateLaunchTemplateVersion
        ec2:CreateRoute
        ec2:DeleteFleets
        ec2:DeleteLaunchTemplate
        ec2:DeleteLaunchTemplateVersions
        ec2:DescribeInternetGateways
        iam:GetInstanceProfile

.. dropdown:: Extra GCP Policy 
    
    .. code-block::

        compute.instanceTemplates.create
        compute.instanceTemplates.delete
        compute.instanceTemplates.get
        compute.instanceTemplates.useReadOnly
        compute.globalOperations.get
        compute.globalOperations.getIamPolicy
        compute.globalOperations.list

The full policy documents can be found here: :ref:`GCP <gcp-policy-doc>`  /  :ref:`AWS <aws-iam-policy>`

After this opt in to V2 by changing your import:

.. code-block:: python

    # from coiled import Cluster
    from coiled.v2 import Cluster

    cluster = Cluster(scheduler_vm_types=["t3.medium"], worker_vm_types=["t3.medium"])
    cluster.close()


V2 is major rewrite of our internal systems. These include a few breaking
changes and many significant improvements.

Continued Support of V1
-----------------------

We will continue to support the original Coiled system for some months to allow you to adapt your workflows and make any required changes. We want to ensure a smooth experience and don't expect many breaking changes.

If you want to stay with the existing system, even after V2 is launched, pin
your ``coiled`` library to ``<0.2`` in your Python environment:

.. code-block:: python

    coiled < 0.2

Known Issues
------------

While we roll out support for V2 to early beta users please be aware that we
have not yet implemented everything from V1. These will be launched before the
final rollout in May.

- GPU support is not implemented.
- Spot instance support is not implemented.
- ``worker_class`` parameter is not implemented.
- ``use_scheduler_public_ip`` is not implemented.
- ``protocol`` parameter is not implemented.
- ``environ`` parameter is not implemented.
- Fetching GCP cluster logs is disabled temporarily.


Deprecations
------------

Cluster configurations have been deprecated so the ``configuration`` argument is no longer allowed.
Instead, configuration is now directly passed to the ``Cluster`` class at creation time.

API Reference
-------------

.. autoclass:: coiled._beta.cluster.ClusterBeta
.. autoclass:: coiled._beta.core.BackendOptions
.. autoclass:: coiled._beta.core.AWSOptions
.. autoclass:: coiled._beta.core.FirewallOptions
