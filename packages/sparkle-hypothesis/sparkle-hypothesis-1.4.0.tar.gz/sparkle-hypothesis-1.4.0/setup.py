# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparkle_hypothesis']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=6.42.2,<7.0.0', 'sparkle-test>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'sparkle-hypothesis',
    'version': '1.4.0',
    'description': 'Use the power of hypothesis property based testing in PySpark tests',
    'long_description': "# sparkle-hypothesis\nHypothesis for Spark Unit tests\n\nLibrary for easily creating PySpark tests using Hypothesis. Create heterogenious test data with ease\n\nInstallation:\n```bash\npip install sparkle-hypothesis\n```\n\n## Example\n```python\nfrom sparkle_hypothesis import SparkleHypothesisTestCase, save_dfs\n\nclass MyTestCase(SparkleHypothesisTestCase):\n    st_groups = st.sampled_from(['Pro', 'Consumer'])\n\n    st_customers = st.fixed_dictionaries(\n        {'customer_id:long': st.integers(min_value=1, max_value=10),\n        'customer_group:str': st.shared(st_groups, 'group')})\n\n    st_groups = st.fixed_dictionaries(\n        {'group_id:long': st.just(1),\n         'group_name:str': st.shared(st_groups, 'group')\n         })\n\n    @given(st_customers, st_groups)\n    @save_dfs()\n    def test_answer_parsing(self, customers: dict, groups:dict):\n        customers_df = self.spark.table('customers')\n        groups_df = self.spark.table('groups')\n```\n",
    'author': 'Machiel Keizer Groeneveld',
    'author_email': 'machielg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/machielg/sparkle-hypothesis/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
