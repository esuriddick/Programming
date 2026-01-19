function generateCheatBlockLatex(block)
    local title = pandoc.utils.stringify(block.attributes["title"])
    
    -- create a small Pandoc-Document with block.content
    local pandocDocument = pandoc.Pandoc(block.content, {})

    -- use pandoc.write to convert into LaTeX
    local latexContent = pandoc.write(pandocDocument, "latex")

    local latexCode = "\\begin{tikzpicture}\n"
    latexCode = latexCode .. "    \\node [mybox] (box){%\n"
    latexCode = latexCode .. "        " .. latexContent .. "};\n"
    latexCode = latexCode .. "    \\node[fancytitle, right=10pt] at (box.north west) {" .. title .. "};\n"
    latexCode = latexCode .. " \\end{tikzpicture}"
    latexCode = latexCode .. "\\vspace{5pt}"

    return pandoc.RawBlock('latex', latexCode)
end

function replaceCheatBlock(block)
    local blockType = block.classes[1]

    if blockType == "cheat" then
        return generateCheatBlockLatex(block)
    else
        return block
    end
end

-- add filter to Pandoc
return {
    { Div = replaceCheatBlock }
}
