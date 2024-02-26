

⚠️Deprecated: Hugo has officially supported math blocks([docs](https://gohugo.io/content-management/mathematics/)), this repo is no longer useful.

# Hugo Math Patch

Add support for math formula wrapped in `$..$` (inline) and `$$...$$`(multiline), which means you don't have to type `\\\\` in math for a real `\\` or add extra shortcode.

This feature is credited to [goldmark-qjs-katex](https://github.com/graemephi/goldmark-qjs-katex), and this patch script just adds goldmark-qjs-katex to the [official hugo source code](https://github.com/gohugoio/hugo).

A Github Action is configured to automatically check latest hugo release, patch with katex support and then build (extended version).
You can download the executables from [the Release Page](https://github.com/du33169/hugo-math-patch/releases).

Warning: these executables are built according to [the contributing guides of hugo](https://github.com/gohugoio/hugo/blob/master/CONTRIBUTING.md#building-hugo-with-your-changes), and they may behave differently with official hugo production release.

## Usage

1. Download the compiled [hugo executable (with math support)](https://github.com/du33169/hugo-math-patch/releases).
2. Copy to your hugo blog directory. Or replace the global installed hugo if you prefer.

3. Include css files required by katex. Refer to [KaTeX Stylesheet](#katex-stylesheet).

4. Use as normal hugo, but ensure you invoke the proper executable


### disable katex support

In hugo `config.toml`:
```toml
[markup.goldmark.extensions]
katex = false
```
#### KaTeX Stylesheet

The patched hugo executable only convert math formula in Markdown to katex html. To properly render it, you need to **include the KaTeX stylesheet into the page**. 

Some themes has already included katex support(but need extra shortcodes or something). Just enable it and the themes will include katex css themselves. 

Most themes also support adding custom CSS. You can use a CDN link, such as https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css.

So check their docs. If you are unlucky, you can still follow these two tutorials to manually write templates and add CSS:

- [Add Custom CSS Or Javascript To Your Hugo Site](https://www.banjocode.com/post/hugo/custom-css)
- https://hugo-mini-course.netlify.app/sections/styling/custom/

## Manual Patching

1. put `patch_katex.py` in top level of hugo source code directory
2. `python3 patch_katex.py`

## What does the patch script do?

Adds goldmark-qjs-katex to dependencies, This will update 2 files: `go.mod` and `go.sum`.

```bash
go get github.com/graemephi/goldmark-qjs-katex
```

Modifies `markup/goldmark/goldmark_config/config.go`: adds enable config field `Katex`.

```go
var Default = Config{
	Extensions: Extensions{
        KaTeX:           false,//added
		...//omit multiple lines
	},
}
    ...//omit multiple lines
type Extensions struct {
	KaTeX           bool//added
    ...//omit multiple lines
}
```

Modifies `markup/goldmark/convert.go`: adds `goldmark-qjs-katex` to import list, and the control logic deciding whether to enable katex extension or not.

```go
package goldmark

import (
	"bytes"
	...//omit multiple lines
	qjskatex "github.com/graemephi/goldmark-qjs-katex"//added
)
...//omit multiple lines

extensions = append(extensions, images.New(cfg.Parser.WrapStandAloneImageWithinParagraph))
//start insertion
if cfg.Extensions.KaTeX {
    extensions = append(extensions, &qjskatex.Extension{})
}
//end insertion
```

## Acknowledgements

- [Hugo](https://github.com/gohugoio/hugo) 
- [goldmark-qjs-katex](https://github.com/graemephi/goldmark-qjs-katex)
- inspired by [a hugo PR from @awwong1](https://github.com/gohugoio/hugo/pull/6842) 
