from setuptools import setup

DISTNAME = "grplot"
VERSION = "0.1.8"
MAINTAINER = "Ghiffary Rifqialdi"
MAINTAINER_EMAIL = "grifqialdi@gmail.com"
DESCRIPTION = "grplot: lazy statistical data visualization"
LICENSE = 'BSD (3-clause)'
URL = "https://github.com/ghiffaryr/grplot"
PROJECT_URLS = {
                "Bug Tracker": "https://github.com/ghiffaryr/grplot/issues"
               }
CLASSIFIERS = [
               'Intended Audience :: Science/Research',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8',
               'Programming Language :: Python :: 3.9',
               'License :: OSI Approved :: BSD License',
               'Topic :: Scientific/Engineering :: Visualization',
               'Topic :: Multimedia :: Graphics',
               'Operating System :: OS Independent',
               'Framework :: Matplotlib',
              ]
DOWNLOAD_URL = "https://github.com/ghiffaryr/grplot"
PYTHON_REQUIRES = ">=3.7"
INSTALL_REQUIRES = [
    'numpy>=1.22.3',
    'matplotlib>=3.5.1',
    'seaborn>=0.11.2',
    'squarify>=0.4.3',
    'pandas>=1.4.1',
]
EXTRAS_REQUIRE = {
                  'all': [
                          'scipy>=1.2',
                          'statsmodels>=0.9',
                         ]
                 }
PACKAGES = ["grplot",
            "grplot.features",
            "grplot.features.add.label_add",
            "grplot.features.add.log_label_add",
            "grplot.features.add.statdesc_add",
            "grplot.features.add.text_add",
            "grplot.features.add.tick_add",
            "grplot.features.alpha",
            "grplot.features.dt",
            "grplot.features.font",
            "grplot.features.log",
            "grplot.features.padding",
            "grplot.features.plot",
            "grplot.features.rot",
            "grplot.features.sep.statdesc_sep",
            "grplot.features.sep.text_sep",
            "grplot.features.sep.tick_sep",
            "grplot.features.statdesc",
            "grplot.features.text",
            "grplot.features.title",
            "grplot.hotfix",
            "grplot.utils",
           ]

if __name__ == "__main__":

    from setuptools import setup

    import sys
    if sys.version_info[:2] < (3, 7):
        raise RuntimeError("grplot requires python >= 3.7.")

    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
    )