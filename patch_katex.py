import subprocess

# Step 1: Add goldmark-qjs-katex dependency
subprocess.run(["go", "get", "github.com/graemephi/goldmark-qjs-katex"])

# Step 2: Modify markup/goldmark/convert.go
convert_go_file = "markup/goldmark/convert.go"  # Update with the actual path
with open(convert_go_file, "r") as f:
    lines = f.readlines()

# Add import statement
import_line = '\tqjskatex "github.com/graemephi/goldmark-qjs-katex"\n'
import_insert_index=lines.index('import (\n')
while lines[import_insert_index]!=')\n':
	import_insert_index+=1
import_insert_index-=1
print(f'preview import position\n>>>\n{lines[import_insert_index]}{import_line}{lines[import_insert_index+1]}<<<\n')
lines.insert(import_insert_index+1, import_line)

# Modify plugin list
plugin_lines = '''	if cfg.Extensions.KaTeX {
		extensions = append(extensions, &qjskatex.Extension{})
	}
'''
plugin_insert_index = lines.index("\textensions = append(extensions, images.New(cfg.Parser.WrapStandAloneImageWithinParagraph))\n")
print(f'preview plugin_insert position\n>>>\n{lines[plugin_insert_index]}{plugin_lines}{lines[plugin_insert_index+1]}<<<\n')

lines.insert(plugin_insert_index+1,plugin_lines)

# Write back to the file
with open(convert_go_file, "w") as f:
    f.writelines(lines)

# Step 3: Modify markup/goldmark/goldmark_config/config.go
config_go_file = "markup/goldmark/goldmark_config/config.go"  # Update with the actual path
with open(config_go_file, "r") as f:
    lines = f.readlines()

# Modify default config
default_config_lines = '\t\tKaTeX:           true,\n'
default_config_index = lines.index("\tExtensions: Extensions{\n")
print(f'preview extension_config position\n>>>\n{lines[default_config_index]}{default_config_lines}{lines[default_config_index+1]}<<<\n')

lines.insert(default_config_index+1,default_config_lines)

# Modify extensions struct
extensions_struct_lines = '\tKaTeX           bool\n'
extensions_struct_index = lines.index("type Extensions struct {\n")
print(f'preview extensions_struct position\n>>>\n{lines[extensions_struct_index]}{extensions_struct_lines}{lines[extensions_struct_index+1]}<<<\n')

lines.insert(extensions_struct_index+1,extensions_struct_lines)

# Write back to the file
with open(config_go_file, "w") as f:
    f.writelines(lines)
