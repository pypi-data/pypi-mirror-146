import time
import os
import pickle
from io import StringIO
import sys
import time
import os
from shutil import copyfile
import __main__ as main
# print()

import importlib.resources as res
import pydbeamer

latexfile = "pythonhighlight.sty"
if not os.path.exists(latexfile):
	pythonfile = res.open_text(pydbeamer, latexfile, encoding='utf-8', errors='strict')
	copyfile(pythonfile.name, os.getcwd() + '/' + latexfile)

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False
class Base:
	'''
	latex对象的基类Base, 定义各种类一些共同的函数
	'''
	def __init__(self, *item):
		'''
		Base构造函数
		不定长参数插入任意数目的latex对象
		'''
		self.items = list(item)
		self.start = "\n"
		self.end = "\n" 

	def __call__(self, *item):
		'''
		定义此函数, 定义变量像函数使用的行为
		例如f(b1, b2), f是当前的对象, b1,b2是插入其中的latex对象
		返回值: self, 使返回的对象能够继续被插入其上层的对象
		'''
		self.insert(*item)
		return self


	def insert(self, *item):
		'''
		输入: 插入的latex对象列表
		输出: 无
		#插入的时候判断待插入的Frame是上一次编译存在的或是新加入的
		#可以有一个或多个Frame待编译
		'''
		for it in item:
			if type(it) == Image:
				if it.created:
					self.items.append(it)
			else:
				self.items.append(it)

	def i(self, *item):
		'''
		insert函数的简化版本
		'''
		self.insert(*item)

	def __str__(self):
		'''
		每个对象转化为字符串的方法, 使用start开始, end结束, 中间为其中的各种latex对象
		如果item中有嵌套, 会继续调用它的__str__方法
		'''
		output = self.start
		# if type(self) == Section:
		# 	print(type(self), self.title)
		for item in self.items:
			if type(item) == Frame:
				framestr = str(item)
				key = self.title + "/" + item.title + str(item.getchildno()) + framestr
				if Document.partialbuild: #如果文档部分编译
					#判断key是否在Frame字典中
					if key not in Document.framedict or item.rebuild:
						output += framestr + "\n"
				else:
					output += framestr + "\n"
				Document.framedict[key] = 1
			else:
				# if key not in Document.framedict:
				output += str(item) + "\n"
		output += self.end
		return output

	def __enter__(self):#为什么要定义__enter__？
		return self

	def getN(self): #获取item的数量, 便于计算incremental显示的帧数
		return 1

	def setstart(self, n):

		self.sindex = n
		previous = n
		for item in self.items:
			if type(item) == str: continue

			item.setstart(previous)
			if item.getN():
				previous += item.getN()
			else:
				previous += 1
	def getchildno(self):
		n = 0
		for item in self.items:
			n += 1
			if isinstance(item, Base):
				n += item.getchildno()
		return n





class Columns(Base):
	'''
	定义Beamer 多列显示类
	'''
	def __init__(self):
		self.start = "\\begin{columns}\n"
		self.end = "\\end{columns}\n"
		self.items = []

class Column(Base):
	'''
	定义Beamer 多列显示的其中一列类, 默认宽度为0.5
	'''
	def __init__(self, *arg, ratio = 0.5):
		self.start = "\\begin{column}{" + str(0.5) + "\\linewidth}\n"
		self.end = "\\end{column}\n"
		self.items = list(arg)

class Equation(Base):
	'''
	定义一个latex公式的显示
	'''
	def __init__(self,eq):
		self.items = [eq]
		self.start = "\\begin{equation}\n"
		self.end = "\\end{equation} \n"

class EqPlus(Base):
	'''
	定义多行公式的显示
	'''
	def __init__(self, nono = '*', plus = False, sindex = 0):
		self.items = []
		self.start = "\\begin{align" + nono + "}\n"
		self.end = "\\end{align" + nono + "}\n"
		self.sindex = sindex
		self.plus = plus

	def __str__(self):
		output = ""
		if not self.plus:
			output += self.start
			for item in self.items:
				output += item + " \\\\"
			output += self.end
		else:
			output = self.displus(self.sindex)
		return output

	def displus(self, start):
		'''
		多行公式的逐行显示输出
		'''
		output = ""
		for i in range(len(self.items)):
			oi = "\\only<" + str(start + i) + ">{ \n"
			oi += self.start 
			for j in range(i):
				oi += str(self.items[j]) + " \\\\ \n"
			oi += str(self.items[i]) + "\n"
			oi += self.end
			oi += "}\n"
			output += oi
		return output

	def getN(self):
		if self.plus:
			return len(self.items)



class Equations(Base):
	def __init__(self):
		self.items = []
		self.start = "\\begin{equation}\n \\left\\{ \n \\begin{array}{c} \n"
		self.end = "\\end{array} \n \\right. \n \\end{equation} \n"

	def __str__(self):
		output = self.start
		for item in self.items:
			output += item + " \\\\"
		output += self.end
		return output


class Table(Base):
	def __init__(self, head, contents, title = None):
		self.start = "\\begin{table}[H]\n"
		self.start += "\\centering\n"
		if not (title == None):
			self.start += "\\caption{\\textbf{" + title +"}}\n"
		n = len(head)
		self.start += "\\begin{tabular}{" + "c" * n + "}\n"
		self.start += "\\hline\n"
		headstr = StringIO()
		print(*head, sep="& ", file = headstr)
		self.start += headstr.getvalue().replace("\n","") + "\\\\\n"
		self.start += "\\hline \n"

		self.end = "\\hline\n"
		self.end += "\\end{tabular}\n"
		self.end += "\\end{table}"
		self.table = contents
		self.items = []

	def __str__(self):
		output = self.start
		table = ""
		for item in self.table:
			out = StringIO()
			print(*item, sep="& ", file = out)
			table += out.getvalue().replace("\n", "") + "\\\\ \n"
		output += table
		output += self.end
		return output



class Section(Base):
	def __init__(self, title):
		self.title = title
		self.items = []
		self.start = "\\section{" + self.title + "}\n"
		self.end = "\n"

class SubSection(Base):
	def __init__(self, title):
		self.title = title
		self.items = []
		self.start = "\\subsection{" + self.title + "}\n"
		self.end = "\n"

class Only(Base):
	def __init__(self, order):
		self.items = []
		self.order = order
		self.start = "\\only<" + str(order) + ">{\n"
		self.end = "}\n"

class OnlyOne(Base):
	def __init__(self, *arg, sindex = 0):
		self.items = list(arg)
		self.sindex = sindex

	def __str__(self):
		n = len(self.items)
		output = ""
		previous = self.sindex
		for i in range(n):
			if i > 0:
				if type(self.items[i-1]) != str:
					previous += self.items[i - 1].getN()
				else:
					previous += 1		
			# print(i, self.items[i], self.items[i].getN())			
			if type(self.items[i]) != str and self.items[i].getN():
				endindex = str(previous + self.items[i].getN()) 
				output += "\\only<{" + str(previous + 1) + "-" + endindex + "}>{\n"
			else:
				output += "\\only<{" + str(previous + 1) + "}>{\n"
			if type(self.items[i]) != str:
				self.items[i].setstart(previous + 1)

			output += str(self.items[i])
			output += "}\n\n"
		return output

	def getN(self):
		return len(self.items)






class OnlyPlus(Base):
	def __init__(self, *items, sindex = 0):
		self.items = list(items)
		self.sindex = sindex

	def __str__(self):
		n = len(self.items)
		output = ""
		previous = self.sindex
		for i in range(n):
			if i > 0:
				if type(self.items[i-1]) != str:
					previous += self.items[i - 1].getN()
				else:
					previous += 1
			if type(self.items[i]) != str:
				output += "\\only<{" + str(previous + 1) + "-}>{\n"
				self.items[i].setstart(previous + 1)
			else:
				output += "\\only<{" + str(previous) + "-}>{\n"

			output += str(self.items[i])
			output += "}\n"
		return output

class iExpression(OnlyPlus):
	def __init__(self, content, sindex = 1):
		items = content.split("\t")
		OnlyPlus.__init__(self, sindex = sindex)
		for item in items:
			self(item)
	def getN(self):
		return len(self.items)


class BaseBox(Base):
	def getN(self):
		N = 0
		for item in self.items:
			n = item.getN() if type(item) != str else 1
			if n:
				N += n
			else:
				N += 1
		return N 

	def __call__(self, *item):
		'''
		定义此函数, 定义变量像函数使用的行为
		例如f(b1, b2), f是当前的对象, b1,b2是插入其中的latex对象
		返回值: self, 使返回的对象能够继续被插入其上层的对象
		'''
		for obj in item:
			self.insert(obj)
			if type(obj) == PythonBlock or type(obj) == PythonBlockPlus:
				self.title += " " + obj.url
				if not Document.forClass:
					obj.setstart(-1)
				obj.setparent(self)
			elif type(obj) == ItemList or type(obj) == NumList:
				if not Document.forClass:
					obj.setstart(-1)


		return self

	def __str__(self):
		'''
		每个对象转化为字符串的方法, 使用start开始, end结束, 中间为其中的各种latex对象
		如果item中有嵌套, 会继续调用它的__str__方法
		'''
		output = self.start.replace("<title>", self.title)
		for item in self.items:
			output += str(item) + "\n"
		output += self.end
		return output



class Box(BaseBox):
	def __init__(self, title, *arg):
		self.items = list(arg)
		self.start = "\\begin{beamerboxesrounded}[shadow=true]{<title>}\n" 
		self.end = "\\end{beamerboxesrounded}\n"
		self.title = title


class RedBox(BaseBox):
	def __init__(self, title, *arg):
		self.items = list(arg)
		self.start = "\\begin{alertblock}{<title>}\n" 
		self.end = "\\end{alertblock}\n"
		self.title = title

class GreenBox(BaseBox):
	def __init__(self, title, *arg):
		self.items = list(arg)
		self.start = "\\begin{exampleblock}{<title>}\n" 
		self.end = "\\end{exampleblock}\n"
		self.title = title

class Image(Base):
	path = "."
	sspath = "." #存放截图路径
	
	def __init__(self, *paths,  ratio = 1,  catption = None):
		if len(paths) > 0:
			path = paths[0]
			figname = path.split("/")[-1]
			#查看图片路径是否存在当前图片, 如果没有则生成图片
			if not os.path.exists(Image.path + figname  + ".png"):
				self.created, n = Image.create(figname)
			else:
				self.created = True

		self.start = "\\begin{center}\n"
		self.end = "\\end{center}\n"
		self.ratio = ratio
		self.catption = catption
		self.paths = paths
		self.items = []
		

	def create(newfile = None, animate = False):
		import os
		figdict = {}
		if os.path.exists("figure.pkl"):
			with open ("figure.pkl", 'rb') as f: #打开文件
				figdict = pickle.load(f) #将二进制文件对象转换成 Python 对象
			f.close()
		if newfile != None and (not (newfile in figdict)):
			#查看截图的路径下面的文件列表
			names = os.listdir(Image.path)
			if len(names) == 0:
				return False, figdict.get(newfile, 0)
			#建立文件名与常见时间映射的字典
			createTime = {(Image.path + name) : os.path.getctime(Image.path + name) for name in names}
			newCreated = {}

			#查找原来文件名前缀的字典里面， 是否存在当前前缀
			for key in createTime:
				if not key.endswith(".png"):
					continue
				ckey = key.split("/")[-1].replace(".png", "")
				ckey = ckey.split("_")[0]
				if not (ckey in figdict):
					newCreated[createTime[key]] = key

			#对截图文件夹里面的新图片按时间进行排序, 选取最早的一张图片修改名字
			if len(newCreated) > 0:
				sortedKeys = sorted(newCreated.keys())
				n = 0
				for key in sortedKeys:
					latest = newCreated[key]
					latestKey = latest.split("/")[-1].replace(".png","")
					tmpfile = newfile
					if not tmpfile.endswith(".png"):
						if animate:
							tmpfile += "_" + str(n)
						tmpfile += ".png"
					os.rename(latest, Image.path + "/" + tmpfile)
					n += 1
					if not animate:
						break

			else:
				return False, figdict.get(newfile, 0)	
			if not n == -1:
				figdict[newfile] = n

		else:
			return False, figdict.get(newfile, 0)
			
		f = open ("figure.pkl", 'wb')
		pickle.dump(figdict, f)
		f.close()
		return True, figdict.get(newfile, 0)

	def __str__(self):
		output = self.start
		for path in self.paths:
			output += "\\includegraphics[width=" + str(self.ratio) +"\\linewidth]{" + Image.figdir + path +"}\n"
		if self.catption != None:
			output += "\\captionof{figure}{" + self.catption +"}\n"
		output += self.end
		return output


class Animate:
	def __init__(self, figname, ratio = 1):
		self.created, n = Image.create(figname, True)
		self.start = "\\begin{center} \n"
		if n != 0:
			self.start += "\\animategraphics[width=1\\linewidth, controls, autoplay]{1}{" + Image.figdir + figname + "_}{1}{" + str(n-1) + "}\n"
		self.end = "\\end{center} \n"

	def __str__(self):
		return self.start + self.end

class PythonBlock(Base):
	pdir = ""
	files = []
	def __init__(self, code, path, head = True):
		self.code = code
		if (not path.endswith(".py")) and (not "." in path):
			path += ".py"
		
		self.name = path
		self.url = ""
		
		self.items = []
		self.parent = None
		self.head = head
		while self.name in PythonBlock.files:
			self.name = self.name.replace(".py", "") + "a" + ".py"
		PythonBlock.files.append(self.name)
		if head:
			self.url =  "\\href{run:"+ "./" + PythonBlock.cpath + self.name +"}{" + "\\footnotesize{\\textit{" + self.name + "}}" +"}\n"
		self.path = PythonBlock.pdir +"/" + self.name
		

	def __str__(self):
		output = ""
		lines = self.code.split("\n")
		lines = [line for line in lines if len(line.strip()) != 0]
		f = open(self.path, "w")
		n = 0
		for line in lines:
			f.write(line +"\n")
		f.close()
		if self.parent == None:
			output += self.url
		output += "\\inputpython{" + self.path + "}{1}{" + str(len(lines)) +"}"

		return output

	def setparent(self, parent):
		self.parent = parent

	def run(self):
		import subprocess
		res = os.popen("python " + self.path).read()
		# res = subprocess.run(['python', self.path])
		self.code += "\n"
		res = res.split("\n")
		for item in res:
			if item.strip() == "":
				continue
			self.code += "#" + item + "\n"

class PythonBlockPlus(PythonBlock):
	'''
	制作渐进显示的代码块
	'''
	def __init__(self, code, path, sindex = 1, head = True):
		'''
		code: 相关代码
		path: 代码路径
		start: 开始的帧数, 默认值为1
		'''
		self.code = code
		# self.path = PythonBlock.pdir +"/" + path
		self.sindex = sindex
		self.name = path
		self.items = []
		self.parent = None
		lines = self.code.split("\n")
		lines = [line for line in lines if line.strip() != ""]
		i = len(lines) - 1
		self.url = ""
		
		self.lines = lines

		while self.name + ".py" in PythonBlock.files:
			self.name = self.name + "a"
		PythonBlock.files.append(self.name + ".py")
		if head:
			self.url = "\\href{run:"+ "./" + PythonBlock.cpath + self.name + ".py" +"}{" + "\\footnotesize{\\textit{" + self.name + ".py" + "}}" +"}\n"
		self.path = PythonBlock.pdir +"/" + self.name

	def __str__(self):
		lines = self.lines
		output = ""
		if self.parent == None:
			output += self.url
		if self.sindex == -1:
			cfile = self.path + ".py"
			f = open(cfile, "w")
			f.write("\n".join(self.lines))
			f.close()
			return "\\inputpython{" + cfile  + "}{1}{" + str(len(lines)) +"} \n"
		for i in range(len(lines)):
			code = ""
			for j in range(i + 1):
				code += lines[j] + "\n"
			if i == len(lines) - 1:
				cfile = self.path + ".py"
			else:
				cfile = self.path + str(i) + ".py"
			try:
				f = open(cfile, "w")
				f.write(code)
				f.close()
			except:
				print("Error",self.path)
			slash = "" if i < len(lines) - 1 else "-"
			output += "\\only<" + str(self.sindex + i) + slash + ">{\n"
			output += "\\inputpython{" + cfile  + "}{1}{" + str(i + 1) +"} \n"
			output += "}\n"
		return output

	def getN(self):
		if self.sindex != -1:
			lines = self.code.split("\n")
			lines = [line for line in lines if line.strip() != ""]
			return len(lines)
		else:
			return 1

	def setstart(self, n):
		if self.sindex != -1:
			self.sindex = n
		# print("set :", n)


class ItemList(Base):
	def __init__(self, *items, sindex = -1):
		self.start = "\\begin{itemize}\n"
		self.end = "\\end{itemize}\n"
		self.sindex = sindex
		self.items = list(items)

	def getN(self):
		if self.sindex != -1:
			return len(self.items)
		return 1

	def __str__(self):
		output = self.start
		prefix = "\\item "
		
		i = self.sindex 
		for item in self.items:
			pre = prefix
			if self.sindex != -1:
				pre = prefix + "<" + str(i) + "-> "
				i += 1
			output += pre + str(item) + "\n"
		output += self.end
		return output

	def setstart(self, n):
		if self.sindex != -1:
			self.sindex = n

class NumList(ItemList):
	def __init__(self, *items, sindex = -1):
		self.start = "\\begin{enumerate}\n"
		self.end = "\\end{enumerate}\n"
		self.sindex = sindex
		self.items = list(items)


class Flow(Base):
	'''
	flow diagram:horizontal
	'''
	def __init__(self, *args, H = True):
		self.start = '''\\smartdiagramset{border color=none,
   uniform color list=teal!60 for 10 items,
   back arrow disabled=true} \n
					'''
		self.start += "\\begin{center}\n"
		direction = ""
		if H:
			direction = ':horizontal'
		self.start += "\\smartdiagram[flow diagram" + direction + "]{"

		self.end = "} \n"
		self.end += "\\end{center} \n"
		self.items = list(args)

	def __str__(self):
		output = self.start
		output += ",".join(self.items)
		output += self.end
		return output




class DescDiagram(Base):
	'''
	descriptive diagram
	'''
	def __init__(self, *args):
		self.start = "\\smartdiagram[descriptive diagram]{ \n"
		self.end = "} \n"
		self.items = list(args)
	def insert(self, item):
		self.items.append(item)
	def __str__(self):
		output = self.start
		for item in self.items:
			output += "{" + ",".join(item) +"},"
		output += self.end
		return output

class Boxed(Base):
	def __init__(self):
		self.items = []
		self.start = "\\begin{framed}"
		self.end = "\\end{framed}"
Mac = 'darwin'
Win = 'win32'
class Frame(Base):
	def __init__(self, title, rebuild = False):
		self.items = []
		self.start = "\\begin{frame}[t]\\frametitle{" + title +"}\n\n"
		self.end = "\\end{frame}\n\n"
		self.title = title
		self.rebuild = rebuild

	def outline(title):
		f = Frame(title)
		contents = '''
        \\tableofcontents[
    currentsection,
    sectionstyle=show/show,
    subsectionstyle=show/show/hide,
  subsubsectionstyle=show/show/hide,
       ]
       '''
		return f(contents)

class TitlePage(Base):
	def __init__(self, title, subtitle):
		self.start = '\\title{' + title +'}\n'
		self.start += '\\author{' + subtitle + '}\n'
		self.end = '\\maketitle'
		self.title = title
		self.subtitle = subtitle
		self.items = []
	def isChinese(self):
		return is_chinese(self.title)


class Document(Base):
	framedict = {}
	partialbuild = True
	def __init__(self, *titles, mainfile, file, forClass = True, partialbuild = True):
		Document.forClass = forClass
		# print("begin:", mainfile)
		mainfile = mainfile.replace("\\","/")
		mainfile = mainfile.split("/")[-1].replace(".py","")
		f = open(file, encoding = 'utf-8')
		self.items = []
		lines = f.readlines()
		self.start = "".join(lines)
		self.start += "\\begin{document}"
		self.end = "\\end{document}"
		self.mainfile = mainfile
		self.initiate()
		self.titles = list(titles)
		self.forClass = forClass
		# self. #初始化Frame字典为空
		if os.path.exists("frame.pkl"):
			with open ("frame.pkl", 'rb') as f: #打开文件
				Document.framedict = pickle.load(f) #将二进制文件对象转换成 Python 对象
			f.close()
		# self.newframe = set()
		Document.partialbuild = partialbuild

		
	def __str__(self):
		'''
		每个对象转化为字符串的方法, 使用start开始, end结束, 中间为其中的各种latex对象
		如果item中有嵌套, 会继续调用它的__str__方法
		'''
		output = self.start


		for title in self.titles:
			output += str(title) + "\n"

		if type(self) == Beamer:
			dct = {True : "主要内容", False : "Outline"}
			self.outline = Frame.outline(dct[self.titles[0].isChinese()])
			output += str(self.outline) + "\n"

		for item in self.items:
			output += str(item) + "\n"
		output += self.end
		return output

	def initiate(self):
		latexdir = "latex"
		codedir = self.mainfile + "/code/"
		Image.figdir =  self.mainfile + "/figure/"
		figdir = Image.figdir
		makedirs(codedir)
		makedirs(figdir)
		makedirs(latexdir)
		if sys.platform == Mac:
			#如果是mac系统, 修改截屏的默认路径和截屏图片的名字
			os.system("/usr/bin/defaults write com.apple.screencapture location " + os.getcwd() + "/" + figdir)
			os.system("/usr/bin/defaults write com.apple.screencapture name " + self.mainfile)	
			Image.path = os.getcwd() +"/"+ figdir
			Image.sspath = Image.path
			PythonBlock.pdir = sys.path[0]+"/"+ codedir
			PythonBlock.cpath = codedir
		elif sys.platform == Win:
			Image.path = os.path.expanduser('~').replace("\\", "/") + "/" + "Pictures"
			Image.sspath = Image.path
			Image.figdir = Image.path
			PythonBlock.pdir =  sys.path[0].replace("\\", "/") + "/" + codedir
			#读取windows截屏路径的配置

	def build(self, repeat = False, build = False, forClass = True):
		Document.forClass = forClass
		ifmac = sys.platform == Mac
		prefix = self.mainfile
		partial = ""
		if Document.partialbuild:
			partial = ".part"
		if self.forClass:
			partial += ".class"
		outfile = prefix + partial + ".tex"
		
		
		pdffile = prefix + partial + ".pdf"
		logfile = prefix + ".latex.log"
		f = open(outfile, "w", encoding = "utf-8")
		f.write(str(self))
		f.close()
		import os
		latexpath = "/Library/TeX/texbin/" if ifmac else ""
		opencmd = "/usr/bin/open " if ifmac else "ii "
		cmdpath = "/bin/" if ifmac else ""
		shfile = "run.sh"
		cmd = "xelatex -interaction=batchmode " + outfile  + "\n"
		from subprocess import run
		
		if repeat: cmd *= 2
		if build:
			res = os.popen(cmd).read()
			f = open(logfile, "w")
			f.write(res)
			f.close()
		# run(cmdpath + "rm " + prefix + ".aux")
		# run(cmdpath + "rm " + prefix + ".log")
		# run(cmdpath + "rm " + prefix + ".out")
		if build:
			if ifmac:
				os.system(opencmd + pdffile)
			else:
				os.startfile(pdffile)

		for f in os.listdir(PythonBlock.pdir):
			if f not in PythonBlock.files:
				os.remove(PythonBlock.pdir + "/" + f)

		f = open ("frame.pkl", 'wb')
		pickle.dump(Document.framedict, f)
		f.close()

		# f.write(cmd)
		# f.close()
		# import os
		# print(cmdpath + "sh " + os.getcwd() + "/"+ shfile)
		# os.system(cmdpath + "sh " + os.getcwd() + "/"+ shfile)


class Beamer(Document):
	def __init__(self, *titles, mainfile = main.__file__, file = None, forClass = True, partialbuild = False):
		# print(sys._getframe().f_code.co_filename)
		if file == None:
			file = res.open_text(pydbeamer, 'basebeamer.tex', encoding='utf-8', errors='strict')
			file = file.name
		Document.__init__(self, *titles, mainfile = mainfile, file = file, forClass = forClass, partialbuild = partialbuild)

class A4Doc(Document):
	def __init__(self, *titles, mainfile = main.__file__, file = None, forClass = True, partialbuild = True):
		if file == None:
			file = res.open_text(pydbeamer, 'baseA4.tex', encoding='utf-8', errors='strict')
			file = file.name
		Document.__init__(self, *titles, mainfile = mainfile, file = file, forClass = forClass, partialbuild = partialbuild)

def makedirs(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

PB = PythonBlock
PBP = PythonBlockPlus
IL = ItemList
NL = NumList
Im = Image
Fr = Frame

if __name__ == '__main__':
	# print(os.getcwd())
	import __main__ as main
	print(eval('is_chinese'))
	f = Frame("Hello")
	print(isinstance(f, Section))

	# print(dir(__main__))
	# framedict = {}
	# if os.path.exists("frame.pkl"):
	# 	with open ("frame.pkl", 'rb') as f: #打开文件
	# 		framedict = pickle.load(f) #将二进制文件对象转换成 Python 对象
	# 	f.close()
	# framedict = {"s1":"f1","s2":"f2"}
	# hello = {"f1":"f2"}

	# f = open ("frame.pkl", 'wb')
	# pickle.dump(framedict, f)
	# pickle.dump(hello, f)
	# f.close()

	# with open ("frame.pkl", 'rb') as f: #打开文件
	# 	figdict = pickle.load(f) 
	# 	hel = pickle.load(f)#将二进制文件对象转换成 Python 对象
	# f.close()
	# print(figdict)
	# print(hel)


	# ret1 = is_chinese("Ley刘亦菲")
	# print(ret1)

	# ret2 = is_chinese("123刘")
	# print(ret2)


