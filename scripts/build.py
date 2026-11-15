"""Render the bilingual, dependency-free website from reviewed public content."""
from pathlib import Path
import hashlib, json, shutil
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
BASE = 'https://andrew05060414.github.io'

def build():
    data = json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
    evidence = json.loads((ROOT/'content/evidence.json').read_text(encoding='utf-8'))
    projects = json.loads((ROOT/'content/projects.json').read_text(encoding='utf-8'))
    env = Environment(loader=FileSystemLoader(ROOT/'templates'), undefined=StrictUndefined,
                      autoescape=select_autoescape(['html']), keep_trailing_newline=True)
    page = env.get_template('index.html')
    asset_version = hashlib.sha256(b''.join((ROOT/'assets'/name).read_bytes() for name in ('site.css','site.js'))).hexdigest()[:12]
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets', OUT/'assets', dirs_exist_ok=True)
    for lang in ('en', 'zh'):
        zh = lang == 'zh'
        t = data['TX'][lang]
        tiers = [dict(name=x[0],n=x[1],sw=x[2],d=t['tierD'][i]) for i,x in enumerate(data['TIERS'])]
        field = [dict(cls='f '+x['sw'],d=0) for x in tiers for _ in range(x['n'])]
        keys = [dict(id=id,n=f'{i+1:02}',l=t['keys'][i][0],s=t['keys'][i][1]) for i,id in enumerate(data['IDS'])]
        oss = [dict(name=o[0],url=o[1],n=o[2],pct=o[2]/18*100,what=t['ossWhat'][i]) for i,o in enumerate(data['OSS'])]
        ctx = dict(t=t,lang=lang,htmlLang='zh-CN' if zh else 'en',rows=[data['ROW1'],data['ROW2']],assetVersion=asset_version,
                   field=field,tiers=tiers,keys=keys,oss=oss,evidence=evidence,projects=projects[lang],
                   problemLabel='要解决的问题' if zh else 'The problem',
                   engineeringLabel='工程工作' if zh else 'Engineering work',
                   evidenceLabel='证据与边界' if zh else 'Evidence and boundaries',
                   historicalHeading='PXRead 交付流程的历史快照' if zh else 'Historical snapshot of PXRead delivery classifications',
                   featuredLabel='重点项目' if zh else 'Main projects',
                   mech=[dict(i=f'{i+1:02}',s=s) for i,s in enumerate(t['mech'])],
                   beats=[dict(no=f'{i+1:02}',tag=b[0],h=b[1],b=b[2]) for i,b in enumerate(t['beats'])],
                   enCls='' if zh else 'on',zhCls='on' if zh else '',enCurrent='false' if zh else 'page',zhCurrent='page' if zh else 'false',isEn=not zh,isZh=zh,feed=t['feed'][0],
                   themeLabel='切换浅色与深色主题' if zh else 'Switch light and dark theme',
                   themeButton='浅 / 深' if zh else 'Light / Dark',languageLabel='语言' if zh else 'Language',
                   snapshotNote='数据快照 · 2026-10-28。方格表示分类，不表示全部已合并。' if zh else 'Snapshot · 2026-10-28. Squares show classifications, not all merged PRs.',
                   methodLink='查看背景' if zh else 'Read the context',
                   identityLine='CMU ECE 硕士 · AI/ML Systems · 寻找 2027 夏季实习' if zh else 'MS ECE at Carnegie Mellon · AI/ML Systems · Open to summer 2027 internships',
                   historicalPolicy='这张图描述 2026-10-28 的分类；策略和执行方式此后可能变化。' if zh else 'This grid describes classifications as of 2026-10-28. The policy and its operation may have changed since.',
                   privateNote='PXRead、Antiochus 和 Chronicle 是个人项目，当前源码未公开。这里展示经过筛选的概述，不提供私有仓库访问入口。' if zh else 'PXRead, Antiochus, and Chronicle are personal projects whose source is currently private. These are selected overviews, not links to private repositories.',
                   evidenceHeading='部分公开贡献' if zh else 'Selected public contributions',
                   resumeLabel='邮件索取简历' if zh else 'Request my résumé by email',
                   sourceLabel='网站源码' if zh else 'Site source',updatedLabel='网站更新' if zh else 'Site updated',
                   pageTitle='Andrew Wang · 王施元 — AI 基础设施与 LLM 系统' if zh else 'Andrew Wang — AI infrastructure & LLM systems',
                   description='王施元，卡内基梅隆大学 ECE 硕士。LLM 基础设施、后端系统与 AI 辅助开发工具。寻找 2027 夏季实习。' if zh else 'Andrew Wang, MS ECE at Carnegie Mellon. LLM infrastructure, backend systems, and tools for reliable AI-assisted development. Seeking summer 2027 internships.',
                   canonical=BASE+('/zh/' if zh else '/'),skipLabel='跳到正文' if zh else 'Skip to content')
        target = OUT/'zh/index.html' if zh else OUT/'index.html'
        target.parent.mkdir(exist_ok=True)
        target.write_text(page.render(**ctx),encoding='utf-8')
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n',encoding='utf-8')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ('/','/zh/'))+'</urlset>\n',encoding='utf-8')
    (OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found — Andrew Wang</title><link rel="stylesheet" href="/assets/site.css"><main class="not-found"><h1>File not found.</h1><p>This page has moved or does not exist.</p><a href="/">Return to Andrew Wang’s site</a></main></html>',encoding='utf-8')
    print('Built English and Chinese pages in dist/')

if __name__ == '__main__':
    build()
