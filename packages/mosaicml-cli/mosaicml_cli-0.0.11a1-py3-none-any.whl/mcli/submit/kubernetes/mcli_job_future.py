""" Kubernetes Intermediate Job Abstraction """

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, NamedTuple, Optional

import yaml
from kubernetes import client

from mcli import version
from mcli.submit.kubernetes.mcli_job_future_typing import MCLIK8sJobTyping
from mcli.utils.utils_kube_labels import label

if TYPE_CHECKING:
    from mcli.config_objects import MCLISecret


class MCLIVolume(NamedTuple):
    volume: client.V1Volume
    volume_mount: client.V1VolumeMount


class MCLIK8sJob(MCLIK8sJobTyping):
    """ MCLI Job K8s Abstraction """

    def add_volume(self, volume: MCLIVolume):
        self.pod_volumes.append(volume.volume)
        self.container_volume_mounts.append(volume.volume_mount)

    def add_environment_variable(self, environment_variable: client.V1EnvVar):
        self.environment_variables.append(environment_variable)

    def add_port(self, port: client.V1ContainerPort):
        """Open an additional port in the primary container

        Args:
            port (client.V1ContainerPort): Port to open, specified as a V1ContainerPort
        """
        self.ports.append(port)

    def add_secret(self, secret: MCLISecret):
        secret.add_to_job(self)


class MCLIConfigMap(NamedTuple):
    config_map: client.V1ConfigMap
    config_volume: MCLIVolume


@dataclass
class MCLIJob():
    """ Kubernetes Intermediate Job Abstraction """

    name: str = ''
    container_image: str = ''
    working_dir: str = ''
    command: List[str] = field(default_factory=list)
    ttl: int = int(timedelta(days=14).total_seconds())
    parameters: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    ports: List[int] = field(default_factory=list)
    num_nodes: int = 1

    def _get_job_spec(self, node_rank: int, local_world_size: Optional[int], namespace: str) -> MCLIK8sJob:
        job_spec = MCLIK8sJob()
        job_spec.container.image = self.container_image
        job_spec.container.command = ['/bin/bash', '-c']
        job_spec.container.args = self.command
        job_spec.container.name = f'{self.name}-rank{node_rank}'
        job_spec.metadata = client.V1ObjectMeta(name=f'{self.name}-rank{node_rank}')
        job_spec.pod_spec.hostname = f'rank{str(node_rank)}'
        job_spec.pod_spec.subdomain = self.name
        job_spec.spec.ttl_seconds_after_finished = self.ttl
        multiprocessing_env_vars = self.get_multiprocessing_env_vars(node_rank=node_rank,
                                                                     local_world_size=local_world_size,
                                                                     namespace=namespace)
        for env_key, env_value in {**self.environment_variables, **multiprocessing_env_vars}.items():
            job_spec.add_environment_variable(client.V1EnvVar(name=env_key, value=env_value))

        if local_world_size is not None:
            job_spec.add_environment_variable(client.V1EnvVar(name='LOCAL_WORLD_SIZE', value=str(local_world_size)))

        for port in self.ports:
            job_spec.add_port(client.V1ContainerPort(container_port=port, host_port=port))
        return job_spec

    def get_multiprocessing_env_vars(self, node_rank: int, local_world_size: Optional[int],
                                     namespace: str) -> Dict[str, str]:
        env_vars = {}
        if local_world_size is None:
            return env_vars

        env_vars['LOCAL_WORLD_SIZE'] = str(local_world_size)
        if self.num_nodes == 1:
            return env_vars

        env_vars['WORLD_SIZE'] = str(self.num_nodes * local_world_size)
        env_vars['NODE_RANK'] = str(node_rank)
        env_vars['MASTER_ADDR'] = f'rank0.{self.name}.{namespace}.svc.cluster.local'
        env_vars['MASTER_PORT'] = str(7501)
        return env_vars

    def get_job_specs(self, local_world_size: Optional[int], namespace: str) -> List[MCLIK8sJob]:
        return [
            self._get_job_spec(node_rank=node_rank, local_world_size=local_world_size, namespace=namespace)
            for node_rank in range(self.num_nodes)
        ]

    def get_config_map(self) -> MCLIConfigMap:
        data = yaml.dump({k: v for k, v in self.parameters.items() if not k.startswith('_')})
        cm = client.V1ConfigMap(
            api_version='v1',
            kind='ConfigMap',
            data={'parameters.yaml': data},
        )
        cm.metadata = client.V1ObjectMeta(name=self.name)
        cm_volume = client.V1Volume(
            name='config',
            config_map=client.V1ConfigMapVolumeSource(name=self.name),
        )
        cm_mount = client.V1VolumeMount(
            name='config',
            mount_path='/mnt/config',
        )

        return MCLIConfigMap(
            config_map=cm,
            config_volume=MCLIVolume(
                volume=cm_volume,
                volume_mount=cm_mount,
            ),
        )

    def get_service(self) -> client.V1Service:
        svc = client.V1Service(
            api_version='v1',
            kind='Service',
            metadata=client.V1ObjectMeta(name=self.name),
            spec=client.V1ServiceSpec(
                selector={label.mosaic.JOB: self.name},
                cluster_ip=None,
                ports=[client.V1ServicePort(port=7500)],  # This port won't be used, but it still must be valid.
            ))

        return svc

    def get_shared_metadata(self) -> client.V1ObjectMeta:
        labels = {
            label.mosaic.JOB: self.name,
            'type': 'mcli',
            label.mosaic.LAUNCHER_TYPE: 'mcli',
            label.mosaic.MCLI_VERSION: str(version.__version__),
            label.mosaic.MCLI_VERSION_MAJOR: str(version.__version_major__),
            label.mosaic.MCLI_VERSION_MINOR: str(version.__version_minor__),
            label.mosaic.MCLI_VERSION_PATCH: str(version.__version_patch__),
        }
        shared_metadata = client.V1ObjectMeta(labels=labels)
        return shared_metadata
