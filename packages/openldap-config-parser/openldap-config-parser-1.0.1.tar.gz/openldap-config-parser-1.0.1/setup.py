# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openldap_config_parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['slapd-parser = openldap_config_parser.command:cli']}

setup_kwargs = {
    'name': 'openldap-config-parser',
    'version': '1.0.1',
    'description': 'slapd.conf parser for OpenLDAP',
    'long_description': 'openldap-config-parser\n======================\n\nslapd.conf parser for OpenLDAP\n\nRepository\n----------\n\nhttps://github.com/mypaceshun/openldap-config-parser\n\nDocumentation\n-------------\n\nhttps://mypaceshun.github.io/openldap-config-parser\n\nInstall\n-------\n\n::\n\n  python3 -m pip install openldap-config-parser\n\nCommand Usage\n-------------\n\n::\n\n  $ slapd-parser --help\n  Usage: slapd-parser [OPTIONS] TARGET\n\n    TARGET      parse target file\n\n  Options:\n    --version   Show the version and exit.\n    -h, --help  Show this message and exit.\n\n  $ slapd-parser test.slapd.conf\n  [16:45:11] run script                                                                                                           command.py:24\n             SlapdConfig(global_conig={\'include\': [[\'/opt/osstech/etc/openldap/schema/core.schema\'],                              command.py:26\n             [\'/opt/osstech/etc/openldap/schema/cosine.schema\'], [\'/opt/osstech/etc/openldap/schema/nis.schema\'],                              \n             [\'/opt/osstech/etc/openldap/schema/inetorgperson.schema\'], [\'/opt/osstech/etc/openldap/schema/misc.schema\'],                      \n             [\'/opt/osstech/etc/openldap/schema/ppolicy.schema\']], \'moduleload\': [[\'ppolicy\']], \'password-hash\': [[\'{CRYPT}\']],                \n             \'password-crypt-salt-format\': [[\'"$5$%.16s"\']], \'attributeoptions\': [[\'lang-\', \'phonetic\']], \'sortvals\':                          \n             [[\'memberUid\', \'member\', \'host\']], \'access\': [[\'to\', \'dn.exact=""\', \'attrs=supportedSASLMechanisms\', \'by\', \'*\',                   \n             \'none\'], [\'to\', \'dn.subtree=""\', \'by\', \'*\', \'read\']]}, databases=[Database(type=\'bdb\', config={\'suffix\':                          \n             [[\'"dc=example,dc=com"\']], \'rootdn\': [[\'"cn=master,dc=example,dc=com"\']], \'monitoring\': [[\'on\']], \'dbconfig\':                     \n             [[\'set_data_dir\', \'.\'], [\'set_lg_dir\', \'.\']], \'index\': [[\'objectClass\', \'eq\'], [\'modifyTimestamp\', \'eq\'], [\'cn\',                  \n             \'eq,sub\']], \'limits\': [[\'dn="uid=user,dc=example,dc=com"\', \'time=unlimited\', \'size=unlimited\']], \'access\': [[\'to\',                \n             \'*\', \'by\', \'dn="uid=user,dc=example,dc=com"\', \'manage\', \'by\', \'*\', \'break\'], [\'to\', \'attrs=userPassword\', \'by\',                   \n             \'self\', \'=wx\', \'by\', \'anonymous\', \'auth\', \'by\', \'*\', \'none\'], [\'to\', \'*\', \'by\', \'*\', \'none\']], \'overlay\':                         \n             [[\'syncprov\']], \'syncprov-checkpoint\': [[\'128\', \'5\']], \'syncprov-sessionlog\': [[\'128\']], \'serverID\': [[\'1\']],                     \n             \'syncrepl\': [[\'rid=1\', \'provider="ldap://ldap.example.com/"\', \'type=refreshAndPersist\',                                           \n             \'binddn="cn=slave,dc=example,dc=com"\', \'credentials="xxxxx"\']], \'mirrormode\': [[\'on\']]}), Database(type=\'monitor\',                \n             config={\'access\': [[\'to\', \'*\', \'by\', \'dn="uid=user,dc=example,dc=com"\', \'read\', \'by\', \'*\', \'none\']]})])\n\nLibrary Usage\n-------------\n\n::\n\n  from openldap_config_parser.parser import parse\n  from openldap_config_parser.config import SlapdConfig\n\n  result = parse("slapd.conf")\n  assert isinstance(result, SlapdConfig)\n',
    'author': 'KAWAI Shun',
    'author_email': 'shun@osstech.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mypaceshun/openldap-config-parser',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
