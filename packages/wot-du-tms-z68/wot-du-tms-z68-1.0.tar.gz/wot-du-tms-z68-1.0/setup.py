from setuptools import setup, find_packages


setup(
    name='wot-du-tms-z68',
    version='1.0',
    license='MIT',
    author="Dmitry Ulasovets",
    author_email='d.ulasovets@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='TMS Z68 wot project',
)
