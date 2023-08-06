import boto3

from cx_releaser.config.config import Config
from cx_releaser.src.docker_registry import AwsRegistry
from cx_releaser.src.release import Release


def args(parser):
    push = parser.add_parser('push', help='Push release')
    push.add_argument('--equal_tags', help='Additional tags to add to release image', nargs='+')
    push.add_argument('--auto_incr_version', choices=['minor', 'major', 'patch'], default='minor')
    push.add_argument('--on_repository_not_exist', choices=['create', 'raise'], default='raise')
    return parser


def push(tenant, version, conf_path, images=None, equal_tags=None, local_version=None, all_tenants=False,
         auto_incr_version='minor', on_tag_exist=None, on_repository_not_exist=None):
    if tenant is None and all_tenants is False:
        raise ValueError('Specify tenant or pass all_tenants')
    conf = Config(conf_path)
    tenants = [conf.get_by(tenant)] if tenant else list(conf.traverse_envs())
    releases = []
    for tenant_conf in tenants:
        registry = AwsRegistry(boto3.client('ecr', region_name='us-east-1',
                                            aws_access_key_id=tenant_conf['aws_access_key_id'],
                                            aws_secret_access_key=tenant_conf['aws_secret_access_key']))
        version = version or tenant_conf.get('version')
        equal_tags = equal_tags or tenant_conf.get('equal_tags')
        for image in images:
            if ':' in image:
                local, remote = image.split(':')
                all_remote = remote.split(',')
            else:
                local, remote = local_version, image
                all_remote = [remote]
            for remote in all_remote:
                on_tag_exist = on_tag_exist or tenant_conf.get('on_tag_exist')
                release = Release(registry, remote, version, equal_tags=equal_tags,
                                  local_name=local,
                                  incr_version=auto_incr_version,
                                  on_tag_exist=on_tag_exist,
                                  on_repo_not_exist=on_repository_not_exist)
                if not version:
                    release = release.next(remote_sync=True)
                print(f'Preparing release: {release.name} with version: {release.version}')
                releases.append((tenant_conf, release))
    for tenant_conf, release in releases:
        check_is_newest_version, check_is_new_hash = tenant_conf.get('check_is_newest_version'), \
                                                     tenant_conf['check_is_new_hash']
        release.validate_push(check_is_next=check_is_newest_version,
                              check_new_hash=check_is_new_hash)
    for tenant_conf, release in releases:
        release.push()
        print(f'Successfully performed release of {release.name} with version: {release.version} on tenant {release.registry_client.registry_name}')
