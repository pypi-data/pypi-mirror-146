from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'ml_pipeline': 
            [ 'Templates/*.ipynb', 'Templates/*.xlsx' ]
            }
    )