#coding:utf-8
import Base,tools,sys,re
from xml.dom.minidom import Document
reload(sys)
sys.setdefaultencoding('utf8')


TVs=["cctv1","cctv2","cctv3","cctv4","cctveurope","cctvamerica","cctv5","cctv5plus","cctv6","cctv7","cctv8","cctvjilu","cctv10","cctv11","cctv12","cctv13","cctvchild","cctv15"]
##TVs=["cctv1"]
if __name__=="__main__":
    tvdoc=Document()
    ###tv根节点
    tv=tvdoc.createElement("tv")
    tv.setAttribute("generator-info-name","Generated by JayAi ")
    tv.setAttribute("generator-info-url","http://nas.codeasy.cn")
    tvdoc.appendChild(tv)
    ###写入节目列表
    for var in TVs:
        ###channel 标签
        channel=tvdoc.createElement("channel")
        channel.setAttribute("id",var)



        ###display-name
        display_name=tvdoc.createElement("display-name")
        display_name.setAttribute("lang","zh")
        ###display-name 标签中的值
        display_name_var=tvdoc.createTextNode(var.upper())
        display_name.appendChild(display_name_var)
        ###添加到channel节点
        channel.appendChild(display_name)
        ###添加到根标签
        tv.appendChild(channel)
    '''

      <programme start="20180222003800 +0000" stop="20180222012700 +0000" channel="cctv1.cn">
        <title lang="zh">生活早参考-特别节目（生活圈）2018-35</title>
      </programme>

    '''
    ##星期1
    days=tools.getweeklist()
    for var in TVs:

        for day in days:
            parser = Base.createJsonWithTVname(var, day)
            islive, pro = Base.getProgramsWithTV(parser)
            for ele in pro:
                start,stop=Base.getDateWithElement(ele,day)
                pname=Base.getNameOfprograms(ele)

                programme=tvdoc.createElement("programme")
                title = tvdoc.createElement("title")
                text=tvdoc.createTextNode(pname)

                programme.setAttribute("start",start+tools.TIME_ZONE)
                programme.setAttribute("stop", stop + tools.TIME_ZONE)
                programme.setAttribute("channel",var)

                title.setAttribute("lang","zh")

                title.appendChild(text)
                programme.appendChild(title)

                tv.appendChild(programme)

    with open("epg.xml","w") as f:
        repl = lambda x: ">%s</" % x.group(1).strip() if len(x.group(1).strip()) != 0 else x.group(0)
        pretty_str = re.sub(r'>\n\s*([^<]+)</', repl, tvdoc.toprettyxml(indent="\t",encoding="UTF-8"))
        f.write(pretty_str)
