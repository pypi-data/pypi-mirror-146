# noaaco2
This is a tutorial to debut a PyPI application and to validate software reproducibility for climate professions.

noaaco2 is a PyPI application that scrapes the latest dataset from NOAA via the Internet and 
displays a graph for a specified number of months.

The PyPI environment allows PyPI applications to run on Windows, MacOS, and Linux operating systems.
As long as Python is installed on the system, you can use it without being aware of the operating system.

noaaco2 scrapes the latest csv file from the following NOAA site:

ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.csv

noaaco2 can generate a graph with specified months and save it in result.csv and noaaco2.png.

In order to run noaaco2 application, Python must be installed on your system.
# How to install Python and noaaco2
<pre>
Follow the Python installation steps for Windows, WSL on Windows, MacOS, and Linux operating systems.
1. Download a right installation file from miniconda site:
https://docs.conda.io/en/latest/miniconda.html

2. X-server installation is needed.
For Windows 11 or 10,WSL on Windows 11 or 10, MacOS, X-server must be installed.
X-server for Windows and WSL on Windows, install VcXsrv Windows X Server.
You can download it from the following site:
https://sourceforge.net/projects/vcxsrv/
For MacOS, you must install XQuartz via Homebrew or brew command.
For Linux operating systems, X-server is ready so that you don't need to install it.

3. PyPI libraries and applications can be installed by the pip installation command.
($) sign indicates the prompt from your system in the terminal. Open the terminal.
And enter the following command to install noaaco2 application.
$ pip install noaaco2
Since noaaco2 uses PyPI libraries such as numpy, pandas and matplotlib, you must install them.
$ pip install numpy pandas matplotlib
noaaco2 uses bash commands such as wget command so that you must install it.
$ sudo apt install wget
</pre>
# How to run noaaco2
noaaco2 takes a single parameter for specifying the number of months. 
Without the number of months, noaaco2 shows a graph with all months in the dataset.

$ noaaco2 \<number-of-months\>

or

$ noaaco2

For example, 24 months, run the following command.

$ noaaco2 24

<img src='https://github.com/ytakefuji/noaaco2/raw/main/noaaco2.png' width=850 height=340 >
 
