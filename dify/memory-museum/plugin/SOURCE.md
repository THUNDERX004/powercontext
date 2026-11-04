# PowerContext Dify 插件来源

- 上游仓库：`https://github.com/oceanbase/powercontext`
- 固定标签：`powercontext-v1.5.0`
- 固定提交：`729dc4c5548f915785a06c318f8cb7ed6cbea45b`
- 插件源目录：`integrations/dify/plugin`
- 插件标识：`knqiufan/powercontext`
- 插件版本：`0.0.1`
- 构建工具：Dify Plugin CLI `0.6.14`
- 本地包：`powercontext-0.0.1.difypkg`
- 包文件 SHA-256：`1c9157b2d3fa6732842191b411f957abbee3879991d70a43da064ad6fab0ebc3`
- Dify 插件内部 checksum：`47a05503b8aa301ef9ea4d319384ba922634061658fb390848d44d0d54ba1ae1`

构建命令：

```bash
git archive --format=zip \
  --output=powercontext-v1.5.0-plugin.zip \
  powercontext-v1.5.0 integrations/dify/plugin

dify plugin package \
  integrations/dify/plugin \
  -o powercontext-0.0.1.difypkg
```

该插件是 OceanBase PowerContext 仓库提供的官方源码插件。本作品只将其打包为可安装的本地
Dify 插件，没有修改插件 Python 源码。
