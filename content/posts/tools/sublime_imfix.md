Title: 修复arch linux下sublime3不能输入中文的bug
Date: 2014-2-13
Modified: 2014-2-13
Category: tools
Tags: arch, linux, fish, sublime, fcitx
Slug: sublime_imfix
Summary: 通过给sublime3打补丁实现在arch linux平台下利用ficitx输入法输入中文
Author: bigpotato

## 修复arch linux下sublime3不能输入中文的bug
介绍下本文使用的软件环境

- 操作系统：[arch linux][]
- 文本编辑器：[sublime text3][]
- 中文输入法：fcitx-sogoupinyin

[arch linux]: https://www.archlinux.org/
[sublime text3]: http://www.sublimetext.com/3

Sublime是新近崛起的一款轻量级、高度可扩展的编辑器，但在Linux平台下存在不能输入中文的bug，这个bug其实是在sublime中不能正常启动输入法导致的，目前解决办法主要有以下几种：

1. 安装InputHelper插件
    通过sublime的包管理器(package control)安装InputHelper插件，这种做法其实比较蛋疼，它的原理类似与复制粘贴，即先把中文输入到缓冲区再复制到sublime中。
2. 给sublime打补丁
    原理目前还没搞懂，方法是sublime官方论坛上某位大神提出的[解决方案][],本文主要介绍这种方法。
3. 打补丁的sublime安装包
    arch linux最被人们称道就是丰富的软件源和软件更新速度，想这种令人发指的bug在[aur上肯定有解决方案][]，目前aur上已经有了能够正常输入中文，及中文汉化的sublime安装包了。

[解决方案]: http://www.sublimetext.com/forum/viewtopic.php?f=3&t=7006&start=10#p41343
[aur上肯定有解决方案]: https://aur.archlinux.org/packages/sublime-text-dev-imfix/

下面详细介绍下第二种解决方案,把下面的代码保存到sublime3安装目录及/opt/sublime_text_3下面，命名为sublime_imfix.c。

```c
/*
sublime-imfix.c
Use LD_PRELOAD to interpose some function to fix sublime input method support for linux.
By Cjacker Huang <jianzhong.huang at i-soft.com.cn>

gcc -shared -o libsublime-imfix.so sublime_imfix.c  `pkg-config --libs --cflags gtk+-2.0` -fPIC
LD_PRELOAD=./libsublime-imfix.so sublime_text
*/
#include <gtk/gtk.h>
#include <gdk/gdkx.h>
typedef GdkSegment GdkRegionBox;

struct _GdkRegion
{
  long size;
  long numRects;
  GdkRegionBox *rects;
  GdkRegionBox extents;
};

GtkIMContext *local_context;

void
gdk_region_get_clipbox (const GdkRegion *region,
            GdkRectangle    *rectangle)
{
  g_return_if_fail (region != NULL);
  g_return_if_fail (rectangle != NULL);

  rectangle->x = region->extents.x1;
  rectangle->y = region->extents.y1;
  rectangle->width = region->extents.x2 - region->extents.x1;
  rectangle->height = region->extents.y2 - region->extents.y1;
  GdkRectangle rect;
  rect.x = rectangle->x;
  rect.y = rectangle->y;
  rect.width = 0;
  rect.height = rectangle->height; 
  //The caret width is 2; 
  //Maybe sometimes we will make a mistake, but for most of the time, it should be the caret.
  if(rectangle->width == 2 && GTK_IS_IM_CONTEXT(local_context)) {
        gtk_im_context_set_cursor_location(local_context, rectangle);
  }
}

//this is needed, for example, if you input something in file dialog and return back the edit area
//context will lost, so here we set it again.

static GdkFilterReturn event_filter (GdkXEvent *xevent, GdkEvent *event, gpointer im_context)
{
    XEvent *xev = (XEvent *)xevent;
    if(xev->type == KeyRelease && GTK_IS_IM_CONTEXT(im_context)) {
       GdkWindow * win = g_object_get_data(G_OBJECT(im_context),"window");
       if(GDK_IS_WINDOW(win))
         gtk_im_context_set_client_window(im_context, win);
    }
    return GDK_FILTER_CONTINUE;
}

void gtk_im_context_set_client_window (GtkIMContext *context,
          GdkWindow    *window)
{
  GtkIMContextClass *klass;
  g_return_if_fail (GTK_IS_IM_CONTEXT (context));
  klass = GTK_IM_CONTEXT_GET_CLASS (context);
  if (klass->set_client_window)
    klass->set_client_window (context, window);

  if(!GDK_IS_WINDOW (window))
    return;
  g_object_set_data(G_OBJECT(context),"window",window);
  int width = gdk_window_get_width(window);
  int height = gdk_window_get_height(window);
  if(width != 0 && height !=0) {
    gtk_im_context_focus_in(context);
    local_context = context;
  }
  gdk_window_add_filter (window, event_filter, context); 
}
```

把上述代码编译成共享库，bash的编译方法见代码开头的注释，由于在我在arch上使用的是fish shell编译方法略有不同，如下：
`eval sudo gcc -shared -o libsublime_imfix.so sublime_imfix.c  (pkg-config --libs --cflags gtk+-2.0) -fPIC`

编译完成后可以测试下能够启动fcitx输入法 `LD_PRELOAD=./libsublime_imfix.so subl3`

测试成功后既可以修改命令行启动脚本和桌面启动脚本了
对于命令行启动脚本，arch默认`/usr/bin/suml3` 是`/opt/sublime_text_3`的一个符号链接，首先删除该符号链接`sudo rm /usr/bin/subl3`,新建启动脚本命令为subl3，内容如下，其中SUB3_HOME为sublime可执行文件所在目录
```shell
#!/bin/bash

SUB3_HOME=/opt/sublime_text_3
CMD="LD_PRELOAD=./libsublime_imfix.so ./sublime_text"
FILENAME=$1
if [ -n "$1" ]
then 
CMD=${CMD}" "`pwd`/$FILENAME
fi
cd "$SUB3_HOME"
eval $CMD
```

接着修改桌面启动脚本`/usr/share/applications/sublime_text.desktop`

```
[Desktop Entry]
Version=1.0
Type=Application
Name=Sublime Text 3 Dev
GenericName=Text Editor
Comment=Sophisticated text editor for code, markup and prose
Exec=subl3 %F
Terminal=false
MimeType=text/plain;
Icon=sublime-text
Categories=TextEditor;Development;
StartupNotify=true
Actions=Window;Document;

[Desktop Action Window]
Name=New Window
Exec=subl3 -n
OnlyShowIn=Unity;

[Desktop Action Document]
Name=New File
Exec=subl3 --command new_file
OnlyShowIn=Unity;
```

修改完后进行测试，结果如图：
![修复sublime中文输入法测试结果]({filename}/images/sublime_imfix.png)

###参考文献
[1. http://www.sublimetext.com/forum/viewtopic.php?f=3&t=7006&start=10#p41343][1]

[2. https://github.com/zivee/sublime3-fcitx-fix][2]


[1]: http://www.sublimetext.com/forum/viewtopic.php?f=3&t=7006&start=10#p41343
[2]: https://github.com/zivee/sublime3-fcitx-fix