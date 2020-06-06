import re
from bs4 import BeautifulSoup

html = """
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Generator" content="iWeb 1.1.2">
  <title>Home</title>
  <link rel="stylesheet" type="text/css" media="screen" href="Home_files/Home.css">
  <script type="text/javascript" src="Home_files/Home.js"></script>
  <style type="text/css">
<!--
.style1 {font-size: 18px}
.style4 {color: #f6391e}
.style5 {color: #439e00}
#apDiv1 {
	position:absolute;
	width:91px;
	height:55px;
	z-index:1;
	left: 171px;
	top: 7px;
}
#apDiv2 {
	position:absolute;
	width:164px;
	height:115px;
	z-index:1;
}
#apDiv3 {
	position:absolute;
	width:164px;
	height:20px;
	z-index:1;
	left: 283px;
	top: 558px;
	visibility: inherit;
}
#apDiv4 {
	position:absolute;
	width:211px;
	height:27px;
	z-index:1;
	left: 286px;
	top: 33px;
}
.style6 {color: #999999}
#apDiv5 {
	position:absolute;
	width:145px;
	height:19px;
	z-index:1;
	left: 302px;
	top: 13px;
}
#apDiv6 {
	position:absolute;
	width:330px;
	height:24px;
	z-index:1;
	left: 184px;
	top: 104px;
}
.style7 {color: #009900}
.style8 {color: #6da0bb; }
#apDiv7 {
	position:absolute;
	width:54px;
	height:39px;
	z-index:1;
	left: 92px;
	top: 114px;
}
#apDiv8 {
	position:absolute;
	width:64px;
	height:45px;
	z-index:1;
	left: 101px;
	top: 41px;
}
-->
    </style>
  <script src="Scripts/AC_RunActiveContent.js" type="text/javascript"></script>
  <!-- TemplateParam name="id" type="text" value="body_layer" --><!-- TemplateParam name="style" type="text" value="margin-left: 0px; position: relative; width: 700px; z-index: 5; " --><!-- TemplateParam name="apdiv" type="text" value="margin-left: 0px; position: relative; width: 700px; z-index: 5; " --><!-- TemplateParam name="class" type="text" value="graphic_generic_body_textbox_style_default" -->
</head>
  <body style="background: transparent url(Images/BG_Tile.jpg) repeat scroll top left; margin: 0pt; " onload="onPageLoad();">
  <div style="text-align: center; ">
      <div style="margin-bottom: 0px; margin-left: auto; margin-right: auto; margin-top: 0px; overflow: hidden; position: relative;  background: transparent url(Images/Pagefill_Blog.jpg) repeat scroll top left; text-align: left; width: 700px; " id="body_content">
        <div style="height: 94px; margin-left: 0px; position: relative; width: 700px; z-index: 10; " id="header_layer">
          <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
          <div class="graphic_generic_header_textbox_style_default" style="height: 86px; left: 20px; position: absolute; top: 8px; width: 209px; z-index: 1;" id="id1">
            <div>
              <div class="Normal">
                <div class="paragraph Header" style="line-height: 26px; padding-bottom: 0pt; padding-top: 0pt; ">
                  <div align="center">Pinecrest Academy Charter School<br>
                    <span class="style1">South Campus</span><br>
                  </div>
                </div>
              </div>
            </div>
          </div>
          


          <div class="graphic_textbox_style_default" style="height: 55px; left: 234px; position: absolute; top: 22px; width: 466px; z-index: 1;" id="id2">
            <div>
              <div class="graphic_textbox_layout_style_default">
                <div class="paragraph Body" style="line-height: 18px; padding-top: 0pt; ">South Campus 15130 SW 80 ST &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  Telephone: (305) 386-0800</div>
                <div class="paragraph Body" style="line-height: 18px; padding-bottom: 0pt; ">Miami, FL 33193 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Fax: (305) 386-6298 </div>
              </div>
            </div>
          </div>
        </div>
        <div style="height: 74px; margin-left: 0px; position: relative; width: 700px; z-index: 0; " id="nav_layer">
          <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
          <div style="background: transparent url(Images/About_Header_Paper.jpg) repeat scroll top left;  height: 600px; left: 0px; position: absolute; top: -600px; width: 700px; z-index: 1; " class="graphic_shape_style_default" id="id3">
            <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
          </div>
          </div>
        <div style="@@(apdiv)@@" id="@@(id)@@">
          <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
          <div style="height: 1px; line-height: 1px; " class="tinyText">&nbsp;
            <div id="apDiv6">
              <script type="text/javascript">
AC_FL_RunContent( 'codebase','http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,28,0','width','329','height','24','src','Home_files/ASCHOOL1','quality','high','pluginspage','http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash','movie','Home_files/ASCHOOL1' ); //end AC code
</script><embed width="329" height="24" src="Home_files/ASCHOOL1.swf" quality="high" pluginspage="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"> 
<noscript><object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,28,0" width="329" height="24">
            <param name="movie" value="Home_files/ASCHOOL1.swf" />
                <param name="quality" value="high" />
                <embed src="Home_files/ASCHOOL1.swf" quality="high" pluginspage="http://www.adobe.com/shockwave/download/download.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash" width="329" height="24"></embed>
              </object>
            </noscript></div>
          </div>
          <div class="@@(_document['class'])@@" style="margin-left: 188px; margin-top: 272px; position: relative; width: 323px; z-index: 1; ">
            <div>
              <div class="Normal">
                <div class="paragraph Heading_1" style="line-height: 28px; padding-top: 0pt; ">Our Vision</div>
                <div class="paragraph Body" style="line-height: 18px; ">
                  <p>The vision of Pinecrest   Academy South is to&nbsp; create a safe, nurturing, challenging, and stimulating   learning environment.<br>
                  </p>
                </div>
                <div class="paragraph Body" style="line-height: 18px; text-decoration: none;">&nbsp;<span class="paragraph Heading_1" style="line-height: 28px; padding-top: 0pt; ">Our Mission</span></div>
                <div class="paragraph Body" style="line-height: 18px; padding-bottom: 0pt; ">
                  <p>The mission of Pinecrest   Academy South is to provide an innovative, challenging curriculum in a loving   environment that furthers a philosophy of respect and high expectations for all   students, parents, teachers, and staff.</p>
                </div>
              </div>
            </div>
          </div>
          

          <div class="graphic_textbox_style_default" style="height: 600px; left: 529px; position: absolute; top: 97px; width: 171px; z-index: 1;" id="id12">
            <div>
              <div class="graphic_textbox_layout_style_default">
                <div class="paragraph Body" style="line-height: 18px; padding-top: 0pt; "><img src="Home_files/shapeimage_1.png" alt="Resources" title="" id="id4" style="height: 24px; left: 1px; margin-bottom: 6px; margin-right: 2px; position: relative; top: 3px; width: 148px; "><span class="tinyText"> </span></div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; "><span style="color: #f6391e; line-height: 12px; opacity: 1.00; "></span><span style="color: #f6391e; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</span></div>
                <div class="Photo_Album_Titles paragraph" style="line-height: 12px; color: #f6391e; line-height: 12px; opacity: 1.00;"><strong><a href="Parents.html">Parents</a></strong></div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; color: #f6391e; line-height: 12px; opacity: 1.00;">-PTO<a href="forms/Pinecrest Academy Supply list.doc"><br>
                -School Supplies</a><br>
                -Registration<br>
                -Other forms</div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; "><span style="color: #f6391e; line-height: 12px; opacity: 1.00; "><img src="Home_files/shapeimage_2.png" alt="" id="id6" style="height: 1px; width: 150px; "><span class="tinyText"> </span></span><span style="color: #f6391e; line-height: 12px; opacity: 1.00; "></span></div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; ">
                  <div id="apDiv7"><img src="Home_files/Halloween 019.jpg" width="72" height="50"></div>
                <span style="color: #f6391e; line-height: 12px; opacity: 1.00; "></span><span style="color: #f6391e; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</span></div>
                <div class="Photo_Album_Titles paragraph" style="line-height: 12px; color: #f6391e; line-height: 12px; opacity: 1.00;"><strong><a href="Students.html">	Students</a></strong></div>
                <div class="paragraph  style5" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;; font-family: 'Verdana', 'sans-serif'; font-size: 10px; font-style: normal; font-variant: normal; letter-spacing: 0; line-height: 14px; margin-bottom: 0px; margin-left: 9px; margin-right: 0px; margin-top: 0px; opacity: 1.00; padding-bottom: 0px; padding-top: 0px; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none;">&nbsp;<span class="style4">-useful links</span></div>
                <div class="paragraph Body_Bold" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;
                  <p>&nbsp;</p>
                </div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; "><span style="color: #f6391e; line-height: 12px; opacity: 1.00; "><span class="tinyText"> </span></span><span style="color: #f6391e; line-height: 12px; opacity: 1.00; "></span></div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; color: #f6391e; line-height: 12px; opacity: 1.00;"></div>
                <div class="paragraph Photo_Album_Titles" style="line-height: 12px; color: #f6391e; line-height: 12px; opacity: 1.00;"></div>
                <div class="paragraph Body" style="line-height: 18px; "><img src="Home_files/shapeimage_6.png" alt="monthly events" title="" id="id11" style="height: 27px; left: 2px; margin-bottom: 3px; margin-right: 4px; position: relative; top: 1px; width: 146px; "><span class="tinyText"> </span></div>
                <div class="paragraph Body_Small" style="line-height: 12px; padding-bottom: 0pt; color: #e69a00; line-height: 12px; opacity: 1.00;"></div>
              </div>
              <div style="clear: both; height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
            </div>
            <div class="Body_Small paragraph" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"><a href="Students of the Month.html"><strong>Students of the Month</strong></a></div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"><a href="AR.html"><strong>TOP AR Readers&nbsp;</strong></a></div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"></div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">
              <p>JFebruary 5<br>
                -Jean Day Pre-Sale ($4)<br>
                <br>
                February 6<br>
                -Teacher Planning Day<br>
                NO SCHOOL!<br>
                <br>
                February 10<br>
                -FCAT Writing<br>
                <br>
              February 11 &amp; 12<br>
              -FCAT Writing Make Up<br>
              <br>
              February 13<br>
              - Valentine's Day Bake Sale<br>
              All items $1<br>
              <br>
              February 16<br>
              - Presidents Day<br>
              NO SCHOOL!<br>
              <br>
              February 18<br>
              - Papa John's Fmaily Night<br>
              <br>
              February 25<br>
              - PTO Meeting<br>
              <br>
              February 26<br>
              - Spring Pictures<br>
                <br>
                <br>
                <br>
                <br>
                <br>
              </p>
            </div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"></div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
            <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"></div>
          </div>
          


          <div class="graphic_textbox_style_default" style="height: 671px; left: 9px; position: absolute; top: 97px; width: 163px; z-index: 1;" id="id15">
            <div>
              <div class="graphic_textbox_layout_style_default">
                <div class="paragraph Body" style="line-height: 18px; padding-top: 0pt; "><a href="Administration.html"><span style="color: #6da0bb"><img src="Home_files/shapeimage_7.png" alt="ABout US" title="" id="id13" style="height: 25px; left: 1px; margin-bottom: 5px; margin-right: 2px; position: relative; top: 2px; width: 148px; "> </span></a></div>
                <div class="paragraph Body_Bold" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; "><span style="color: #6da0bb"><a href="#">Administration</a></span></div>
                <div class="paragraph Body_Bold style8" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; "><span style="color: #6da0bb"><a href="fac.html">FACULTY</a></span></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"><span class="style7"><a href="Teacher of the Year.html">Teacher of the Year&nbsp;</a></span></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"><a href="Elementary School.html">Elementary School</a><br>
                  <a href="Elementary Teachers.html">-Teachers</a><br>
                  <a href="Elementary School Clubs.html">-Clubs&nbsp;</a> </div>
                  <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"><a href="Middle School.html">Middle School</a><br>
                  <a href="Middle School Teachers.html">-Teachers</a><br>
                  <a href="Middle School Clubs.html">-Clubs&nbsp;                </a></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;"><a href="Home_files/WELLNESS POLICY.pdf">Wellness-Policy</a></div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;"></div>
                <div class="paragraph Body_Small" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; color: #009900; line-height: 12px; opacity: 1.00; text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Bold style7" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;"><span style="color: #009900"><a href="FAQs.html">Frequently Asked Question</a></span></div>
                <div class="paragraph Body_Small" style="line-height: 12px; color: #009900; line-height: 12px; opacity: 1.00; text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body_Small" style="line-height: 12px; color: #439e00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
                <div class="paragraph Body" style="line-height: 18px; "><img src="Home_files/shapeimage_8.png" alt="Calendars" title="" id="id14" style="height: 27px; left: 1px; margin-bottom: 3px; margin-right: 2px; position: relative; top: 1px; width: 148px; "><span class="tinyText"> </span></div>
                <div class="paragraph Body_Bold" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"></div>
                <div class="paragraph Body_Bold" style="line-height: 12px; margin-bottom: 0px; margin-top: 0px; line-height: 12px;  text-decoration: none;"></div>
                <div class="paragraph Body_Bold" style="line-height: 14px; color: #eb7d04; line-height: 14px; opacity: 1.00; margin-bottom: 0px;"><a href="http://www.dadeschools.net/calendars/08-09/08-09_el-sec.pdf" target="_blank">Miami-Dade County Public Schools Calendar</a></div>
                <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
                  <div class="Body_Small paragraph" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"><strong><a href="Home_files/February Calendar1.pdf" target="_blank">February Calendar</a></strong></div>
                <div class="paragraph Body_Small" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;">&nbsp;</div>
                      <div class="Body_Small paragraph" style="line-height: 12px; color: #e69a00; line-height: 12px; opacity: 1.00;  text-decoration: none;"><strong><a href="Home_files/Feb2009 Menu.pdf">February Lunch Menu</a></strong></div>
                <div class="paragraph Body_Bold" style="line-height: 14px; color: #eb7d04; line-height: 14px; opacity: 1.00;">
                  <div class="paragraph Body_Bold" style="line-height: 14px; color: #eb7d04; line-height: 14px; opacity: 1.00;"></div>
                </div>
                <div class="paragraph Body_Bold" style="line-height: 14px; color: #eb7d04; line-height: 14px; opacity: 1.00;"></div>
              </div>
              <div style="clear: both; height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
            </div>
          </div>
          <img src="Images/TopStroke.jpg" alt="" style="border: none; height: 2px; left: 0px; opacity: 1.00; position: absolute; top: 0px; width: 700px; z-index: 1; "><img src="Images/About_ImageBorder.png" alt="Frame" width="299" height="291" id="id16" style="border: none; height: 286px; left: 185px; opacity: 1.00; position: absolute; top: 133px; width: 329px; z-index: 1;"><img src="Home_files/School.jpg" alt="" width="293" height="223" style="border: none; height: 249px; left: 203px; position: absolute; top: 151px; width: 293px; z-index: 1;">
          <div style="height: 84px; line-height: 84px; " class="tinyText"></div>
        </div>
        <div style="height: 103px; margin-left: 0px; position: relative; width: 700px; z-index: 15; " id="footer_layer">
          <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
          <div style="background: transparent url(Images/About_Header_Paper.jpg) repeat scroll top left; height: 70px; left: -2px; position: absolute; top: 34px; width: 700px; z-index: 1;" class="graphic_shape_style_default" id="id17">
            <div style="height: 0px; line-height: 0px; " class="tinyText">&nbsp;</div>
            <div id="apDiv5"><a href="http://www.schoolnotes.com/cgi-bin/schoolinfo-list-new.pl?school=PINECREST%20ACADEMY%20AT%20KENDALL%20GREENS&amp;address=15130%20SW%2080%20ST&amp;city=MIAMI&amp;email=mrslarrauri@hotmail.com&amp;state=FL&amp;zipcode=33193&amp;membership=600&amp;phone=305-567-9362&amp;low=K&amp;high=6&amp;llc="><img src="Images/schoolnotespencil.gif" width="144" height="15"></a></div>
            <div class="style6" id="apDiv4">*Teacher pages are found here.</div>
            <div id="apDiv1"><a href="http://www2.dadeschools.net/index.htm"><img src="Images/mdcps.jpg" width="90" height="56"></a></div>
          </div>
        </div>
      </div>
  </div>




</body></html>
"""

def main():
    soup = BeautifulSoup(html, 'lxml')
    for element in soup.find_all('a', text=re.compile(r"staff|faculty", re.IGNORECASE)):
        print(element.parent)



if __name__ == "__main__":
    main() 

