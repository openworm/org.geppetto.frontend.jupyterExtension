import setuptools
from glob import glob
import fnmatch
import os

#This block copies resources to the server so we avoid jupyter nbextension install --py --sys-prefix jupyter_geppetto
data_files = []
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto/geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/*.js')))
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto/geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/*.vm')))
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto/geppetto/src/main/webapp/build/', glob('src/jupyter_geppetto/geppetto/src/main/webapp/build/fonts/*')))
for root, dirnames, filenames in os.walk('src/jupyter_geppetto/geppetto/src/main/webapp/js/'):
    for filename in fnmatch.filter(filenames, '*'):
        data_files.append(('share/jupyter/nbextensions' + root[3:], [os.path.join(root, filename)]))

data_files.append(('share/jupyter/nbextensions/jupyter_geppetto', glob('src/jupyter_geppetto/geppettoJupyter.css')))
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto', glob('src/jupyter_geppetto/GeppettoJupyter.js')))
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto', glob('src/jupyter_geppetto/index.js')))

setuptools.setup(
    name="jupyter_geppetto",
    version="0.4.1.2",
    url="https://github.com/openworm/org.geppetto.frontend.jupyter",
    author="The Geppetto Development Team",
    author_email="info@geppetto.org",
    description="Geppetto extension for Jupyter notebook",
    license="MIT",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'appnope==0.1.0',
        'backcall==0.1.0',
        'bleach==2.1.4',
        'cycler==0.10.0',
        'decorator==4.3.0',
        'defusedxml==0.5.0',
        'entrypoints==0.2.3',
        'html5lib==1.0.1',
        'ipykernel==4.9.0',
        'ipython==6.5.0',
        'ipython-genutils==0.2.0',
        'ipywidgets==7.4.1',
        'jedi==0.12.1',
        'Jinja2==2.10',
        'jsonschema==2.6.0',
        'jupyter==1.0.0',
        'jupyter-client==5.2.3',
        'jupyter-console==5.2.0',
        'jupyter-core==4.4.0',
        'jupyter-geppetto==0.4.1.2',
        'kiwisolver==1.0.1',
        'lxml==4.2.4',
        'MarkupSafe==1.0',
        'matplotlib==2.2.3',
        'mistune==0.8.3',
        'nbconvert==5.4.0',
        'nbformat==4.4.0',
        'notebook==5.6.0',
        'numpy==1.15.1',
        'ordered-set==3.0.1',
        'pandocfilters==1.4.2',
        'parso==0.3.1',
        'pexpect==4.6.0',
        'pickleshare==0.7.4',
        'prometheus-client==0.3.1',
        'prompt-toolkit==1.0.15',
        'ptyprocess==0.6.0',
        'pyecore==0.8.7',
        'pygeppetto==0.4.1',
        'Pygments==2.2.0',
        'pyparsing==2.2.0',
        'python-dateutil==2.7.3',
        'pytz==2018.5',
        'pyzmq==17.1.2',
        'qtconsole==4.4.1',
        'scipy==1.1.0',
        'Send2Trash==1.5.0',
        'setuptools==39.0.1',
        'simplegeneric==0.8.1',
        'six==1.11.0',
        'terminado==0.8.1',
        'testpath==0.3.1',
        'tornado==5.1',
        'traitlets==4.3.2',
        'wcwidth==0.1.7',
        'webencodings==0.5.1',
        'widgetsnbextension==3.4.1',
        'jupyter==1.0.0',
        'pygeppetto==0.4.1'
    ],
)
