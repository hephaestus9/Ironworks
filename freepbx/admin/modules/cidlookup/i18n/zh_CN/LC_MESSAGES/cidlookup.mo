��    5      �  G   l      �  �  �       
   !     ,     >     P     _     o  7   �     �  	   �     �     W     p     �  $   �  '   �     �     �     �  .   �     +  
   1     <     K     Z  
   _     j     ~  &   �  	   �  0   �     �  -   �     	  o   	  �   �	     
  1   
  �  N
     �     �            :   #     ^     m  &   v  	   �     �     �     �  �  �    r     �  	                  )     9     H  2   W     �     �  e   �     
       	   0     :  6   S     �     �  	   �  4   �     �     �     �                    $     1     8  	   R  7   \  	   �  -   �  	   �  x   �  �   O  	   �  <   �  �  .     �     �     �     �  0   �     0     =     F     c  	   p     z  	   �     0                        %   4   ,            )   +               '         *   "         !                    5      &              3       2                           1   
   	      /   (              #      .         -                           $    A Lookup Source let you specify a source for resolving numeric CallerIDs of incoming calls, you can then link an Inbound route to a specific CID source. This way you will have more detailed CDR reports with information taken directly from your CRM. You can also install the phonebook module to have a small number <-> name association. Pay attention, name lookup may slow down your PBX Add CID Lookup Source Add Source CID Lookup Source CID Lookup source Cache results: CallerID Lookup CallerID Lookup Sources Checking for cidlookup field in core's incoming table.. Database name Database: Decide whether or not cache the results to astDB; it will overwrite present values. It does not affect Internal source behavior Delete CID Lookup source ERROR: failed:  Edit Source Enter a description for this source. FATAL: failed to transform old routes:  HTTP Host name or IP address Host: Migrating channel routing to Zap DID routing.. MySQL MySQL Host MySQL Password MySQL Username None Not Needed Not yet implemented OK Password to use in HTTP authentication Password: Path of the file to GET<br/>e.g.: /cidlookup.php Path: Port HTTP server is listening at (default 80) Port: Query string, special token '[NUMBER]' will be replaced with caller number<br/>e.g.: number=[NUMBER]&source=crm Query, special token '[NUMBER]' will be replaced with caller number<br/>e.g.: SELECT name FROM phonebook WHERE number LIKE '%[NUMBER]%' Query: Removing deprecated channel field from incoming.. Select the source type, you can choose between:<ul><li>Internal: use astdb as lookup source, use phonebook module to populate it</li><li>ENUM: Use DNS to lookup caller names, it uses ENUM lookup zones as configured in enum.conf</li><li>HTTP: It executes an HTTP GET passing the caller number as argument to retrieve the correct name</li><li>MySQL: It queries a MySQL database to retrieve caller name</li></ul> Source Source Description: Source type: Source: %s (id %s) Sources can be added in Caller Name Lookup Sources section Submit Changes SugarCRM Username to use in HTTP authentication Username: deleted not present removed Project-Id-Version: FreePBX 2.5 Chinese Translation
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2011-09-23 09:52+0000
PO-Revision-Date: 2011-04-14 00:00+0800
Last-Translator: 周征晟 <zhougongjizhe@163.com>
Language-Team: EdwardBadBoy <zhougongjizhe@163.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
X-Poedit-Language: Chinese
X-Poedit-Country: CHINA
X-Poedit-SourceCharset: utf-8
 查找源是你指定的用来解析入局的数字主叫ID的源，你可以把一条入局线路与特定的CID源链接起来。在这种工作方式下，你将获得更详细的CDR报告，报告中将包含直接从你的CRM里获取的内容。你也可以安装电话簿模块以提供简易的数字<->名字关联。请注意，名字查找将会减慢你的PBX服务器。 添加CID查找源 添加源 CID查找源 CID查找源 缓存结果： 主叫ID查询 主叫ID查询 正在检查incoming表的cidlookup字段。。。 数据库名 数据库： 设置是否将查询结果缓存到astDB；它将覆盖当前设置。它不影响内部源的行为 删除CID查找源 错误：失败： 编辑源 为此源添加描述。 致命错误：无法转换旧的路由（线路）： HTTP 主机名或者IP地址 主机： 正在将频道路由迁移到Zap DID路由。。。 MySQL MySQL主机 MySQL密码 MySQL用户名 无 没有必要 尚未实现 完成 用于HTTP鉴权的密码 密码： 要请求的文件的路径<br/>例如：/cidlookup.php 路径： HTTP服务器监听的端口（默认为80） 端口： 设置查询字符串，特殊标识符“[NUMBER]”会被替换成主叫号码<br/>例如：number=[NUMBER]&source=crm 设置查询字符串，特殊标识符“[NUMBER]”会被替换成主叫号码<br/>例如：SELECT name FROM phonebook WHERE number LIKE '%[NUMBER]%' 查询： 正在从incoming表中移除废弃的channel字段。。。 选择源的类型，你可以在以下几项中选择：<ul><li>内部：使用astdb查询源，可以使用电话簿模块来填充它</li><li>ENUM：使用DNS来查询CID名字，它使用ENUM查询区域，可以在enum.conf中配置</li><li>HTTP:它执行一个HTTP GET请求，将主叫号码作为参数发送出去，以获取正确的名字</li><li>MySQL：到MySQL数据库中查询主叫姓名</li></ul> 源 源的描述： 源类型： 源：%s (id %s) 可以向呼叫者姓名查找源小节添加源 提交更改 SugarCRM 用于HTTP鉴权的用户名 用户名： 已删除 没有出现 已移除 