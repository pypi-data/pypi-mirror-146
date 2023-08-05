from setuptools import setup, find_packages

setup(name='MASB',
      version='0.0.1',
      description='Multi-Agent Goal-Driven Bidding Environment',
      author='Congcong Zhang SUDA',
      author_email='ccxin_15@163.com',
      url='https://github.com/zcc0105/new_multienv.git',
      packages=find_packages(include='MASB'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['gym', 'numpy-stl']
)
