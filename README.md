# Fulao2数据加密分析与视频播放
1. 解密
   - Mt搜索: payload 
   - 再搜索: path 
   - 进入类: Lcom/ilulutv/fulao2/other/j/b;

2. 经过使用Mt注入功能发现解密方法：
    + ` String a(IvParameterSpec ivParameterSpec, SecretKeySpec secretKeySpec, String str)`
    

##过程：
> * 先在解密类中赛选播放视频的json响应，写入本地(append为：Flase)
> * 通过反编译在播放的activity里面添加一个TextView
> * 自己写一个web播放器实现播放


##**_虽然没技术破解它，为了看高清我想到了其他法子。_**
>###开干：
>进过多方面打入log，找到
>* 加密方式：`AES/CBC/PKCS5Padding`
>*  key：`db6f7f9e5d7a770e0e3497a7d7a077f5`
>*  iv为响应header的`x-vtag`参数
>>拿到`x-vtag`的字符串还要进行Md5加密输出16位操作才是真正的iv  
> 示例：`x-vtag = 162039286`  
> Md5加密后：`f694f7f85b567bd8` 


##添加TextView过程：
1. ###筛选视频json用到的代码需要转成smali代码才能添加进dex：
```
String s1 = "json数据";
String s2 = "video_urls";
if (s1.contains(s2)) {
  // 如果 s1 中包含 s2
  write_data(s1);
  //p2为json数据
  //调用write_data的smali代码    invoke-static {p2}, Lcom/ilulutv/fulao2/other/j/b;->write_data(Ljava/lang/String;)V
}

public static void write_data(String content) {
        try {
            File file = new File(
                    "/storage/emulated/0/MT2/apks/fulao2_video.json");

            // if file doesnt exists, then create it
            if (!file.exists()) {
                file.createNewFile();
            }

            FileWriter fw = new FileWriter(file.getAbsoluteFile());
            BufferedWriter bw = new BufferedWriter(fw);
            bw.write(content);
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```
2. ###添加TextView的代码：
```
1. resources.arsc里面自定义添加一个资源id：例如我定义的为xxxxx
2. 通过开发者助手找到了简介界面的xml为：res/layout/fragment_long_film_description_2.xml
3. 在LinearLayout里面添加一个TextView控件，代码如下：
        <TextView
            android:enabled="true"
            android:textColor="@android:color/black"
            android:id="@xxxxx"
            android:focusable="true"
            android:longClickable="true"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:textIsSelectable="true" />

4. 控制简介面的java类在：Lcom/ilulutv/fulao2/film/PlayerActivity的.method private final c(Landroid/os/Bundle;)V方法里面
    把所保存的json数据显示在简介上，用到的代码：
        .line 15
        const v1, 0xxxxxx
        invoke-virtual {v0, v1}, Landroid/view/View;->findViewById(I)Landroid/view/View;
        move-result-object v1
        check-cast v1, Landroid/widget/TextView;
        invoke-direct {p0}, Lcom/ilulutv/fulao2/film/PlayerActivity;->open_file()Ljava/lang/String;
        move-result-object v2
        invoke-virtual {v1, v2}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
   open_file方法：
        .method private open_file()Ljava/lang/String;
            .registers 6
            .prologue
            .line 32
            new-instance v0, Ljava/io/File;
            const-string v1, "/storage/emulated/0/MT2/apks/fulao2_video.json"
            invoke-direct {v0, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V
            .line 33
            const/4 v2, 0x0
            .line 34
            new-instance v3, Ljava/lang/StringBuffer;
            invoke-direct {v3}, Ljava/lang/StringBuffer;-><init>()V
            .line 36
            :try_start_d
            new-instance v1, Ljava/io/BufferedReader;
            new-instance v4, Ljava/io/FileReader;
            invoke-direct {v4, v0}, Ljava/io/FileReader;-><init>(Ljava/io/File;)V
            invoke-direct {v1, v4}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V
            :try_end_17
            .catch Ljava/io/IOException; {:try_start_d .. :try_end_17} :catch_55
            .catchall {:try_start_d .. :try_end_17} :catchall_46
            .line 38
            :goto_17
            :try_start_17
            invoke-virtual {v1}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;
            move-result-object v0
            if-eqz v0, :cond_2f
            .line 39
            invoke-virtual {v3, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;
            :try_end_20
            .catch Ljava/io/IOException; {:try_start_17 .. :try_end_20} :catch_21
            .catchall {:try_start_17 .. :try_end_20} :catchall_53
            goto :goto_17
            .line 43
            :catch_21
            move-exception v0
            .line 44
            :goto_22
            :try_start_22
            invoke-virtual {v0}, Ljava/io/IOException;->printStackTrace()V
            :try_end_25
            .catchall {:try_start_22 .. :try_end_25} :catchall_53
            .line 46
            if-eqz v1, :cond_2a
            .line 48
            :try_start_27
            invoke-virtual {v1}, Ljava/io/BufferedReader;->close()V
            :try_end_2a
            .catch Ljava/io/IOException; {:try_start_27 .. :try_end_2a} :catch_41
            .line 54
            :cond_2a
            :goto_2a
            invoke-virtual {v3}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;
            move-result-object v0
            :cond_2e
            :goto_2e
            return-object v0
            .line 41
            :cond_2f
            :try_start_2f
            invoke-virtual {v1}, Ljava/io/BufferedReader;->close()V
            .line 42
            invoke-virtual {v3}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;
            :try_end_35
            .catch Ljava/io/IOException; {:try_start_2f .. :try_end_35} :catch_21
            .catchall {:try_start_2f .. :try_end_35} :catchall_53
            move-result-object v0
            .line 46
            if-eqz v1, :cond_2e
            .line 48
            :try_start_38
            invoke-virtual {v1}, Ljava/io/BufferedReader;->close()V
            :try_end_3b
            .catch Ljava/io/IOException; {:try_start_38 .. :try_end_3b} :catch_3c
            goto :goto_2e
            .line 49
            :catch_3c
            move-exception v1
            .line 50
            invoke-virtual {v1}, Ljava/io/IOException;->printStackTrace()V
            goto :goto_2e
            .line 49
            :catch_41
            move-exception v0
            .line 50
            invoke-virtual {v0}, Ljava/io/IOException;->printStackTrace()V
            goto :goto_2a
            .line 46
            :catchall_46
            move-exception v0
            move-object v1, v2
            :goto_48
            if-eqz v1, :cond_4d
            .line 48
            :try_start_4a
            invoke-virtual {v1}, Ljava/io/BufferedReader;->close()V
            :try_end_4d
            .catch Ljava/io/IOException; {:try_start_4a .. :try_end_4d} :catch_4e
            .line 51
            :cond_4d
            :goto_4d
            throw v0
            .line 49
            :catch_4e
            move-exception v1
            .line 5
            invoke-virtual {v1}, Ljava/io/IOException;->printStackTrace()V
            goto :goto_4d
            .line 46
            :catchall_53
            move-exception v0
            goto :goto_48
            .line 43
            :catch_55
            move-exception v0
            move-object v1, v2
            goto :goto_22
        .end method
```
##效果图：
![mahua](C:\Users\plane\Desktop\ad.jpg)
