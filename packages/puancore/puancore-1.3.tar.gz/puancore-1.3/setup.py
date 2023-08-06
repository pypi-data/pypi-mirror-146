from setuptools import setup
from setuptools import Extension

# def configuration(parent_package='', top_path=None):

#     config = Configuration('uFuncs',
#                            'puancore',
#                            top_path)
#     config.add_extension('npufunc', ['puancore/uFuncs/competition_ranking.c'], include_dirs=['/opt/homebrew/Frameworks/Python.framework/Headers', '/opt/homebrew/Cellar/numpy/1.22.3_1/lib/python3.9/site-packages/numpy/core/include/'])

#     return config

if __name__ == "__main__":
    setup(name="puancore",
          version="1.3",
          description = "Hello",
          author = "Moa Stenmark",
          author_email = "moa@ourstudio.se",
          install_requires=["numpy"],
          packages=['puancore', 'puancore/uFuncs'],
          url = "https://oursite.com",
          long_description = """Write something here""",
          ext_modules=[
              Extension(
                    'puancore/uFuncs/npufunc',
                    ['puancore/uFuncs/competition_ranking.c'],
                    include_dirs=['/opt/homebrew/Frameworks/Python.framework/Headers', '/opt/homebrew/Cellar/numpy/1.22.3_1/lib/python3.9/site-packages/numpy/core/include/']
              )
          ]
        #   configuration=configuration
    )