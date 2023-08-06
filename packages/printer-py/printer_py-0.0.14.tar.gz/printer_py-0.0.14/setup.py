from setuptools import setup, find_packages


VERSION = '0.0.14'
DESCRIPTION = 'A printer package helps you to debug using print any number of variables of any types only with comma or other operators you want.'
long_description = '''<div id="description" data-target="project-tabs.content" class="vertical-tabs__content" role="tabpanel" aria-labelledby="description-tab mobile-description-tab" tabindex="-1" style="display: block;">          <h2 class="page-title">Project description</h2>                    <div class="project-description">            <h1>printer_py</h1><p>ready for use !</p><p>Developed by Ninad Goswamy (c) 2022</p><h2>explanation of printer function :<br> Syntax : printer(value1,value2,..,valueN,newline=True/False,operator=","/" "/"&")<br>newline = used to specify newline by default it is false <br>operator: is used to display values by saperating comma or other value , by default it is comma </h2></br><h2>Examples of How To Use the printer function </h2><p>Debugging on server</p><pre><span class="kn">from</span> <span class="nn">printer</span> <span class="kn">import</span> <span class="n">printer</span></br><span class="n">printer</span><span class="o"></span><span class="n"></span><span class="p">(</span><span class="s1">'test'</span><span class="p">,</span> <span class="mi">newln=False</span><span class="p">,operator="=")</span>
</br><span class="n">printer</span><span class="o"></span><span class="n"></span><span class="p">(</span><span class="s1">'test'</span><span class="p">,</span> <span class="mi">9999</span><span class="p">,newline=False)</span>
</br><span class="n">printer</span><span class="o"></span><span class="n"></span><span class="p">(</span><span class="s1">'test'</span><span class="p">,</span> <span class="mi">{"key":4562}</span><span class="p">,newline=True)</span>
</br><span class="n">printer</span><span class="o"></span><span class="n"></span><span class="p">(</span><span class="s1">'test'</span><span class="p">,</span> <span class="mi">9999</span><span class="p">,"default")</span>
</br><span class="n">printer</span><span class="o"></span><span class="n"></span><span class="p">(</span><span class="s1">'newline'</span><span class="p">,</span> <span class="mi">9999</span><span class="p">,newline=True)</span></pre>          </div>                  </div>'''
# Setting up
setup(
    name="printer_py",
    version=VERSION,
    author="Ninad Goswamy (ninsgosai)",
    author_email="<ninad.goswamy@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='',  
    # package_dir={"": "src"},
    # packages = ['src'],
    # packages=setuptools.find_packages(where="src"),
    # packages=setuptools.find_packages(),
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'debug', 'print', 'diffrent type value', 'python debug', 'python2','printer_py','printer-py'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)