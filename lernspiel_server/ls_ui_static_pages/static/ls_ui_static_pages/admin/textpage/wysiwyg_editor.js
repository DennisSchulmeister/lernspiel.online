/*
 * Lernspiel Online: Lecture Game Platform - Core App
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

document.addEventListener("DOMContentLoaded", async function() {
    /**
     * Replace the plain <textarea> of the content field with a proper rich-text
     * editor for the selected format.
     */
    async function toggleContentEditor(container) {
        const formatField  = container.querySelector(".__format");
        const contentField = container.querySelector(".__content");
        
        let currentEditor = {
            markdown: {
                container: null,    // Container to circumvent the flex layout
                toolbar:   null,
                editor:    null,
            },
            html: null,
        };

        async function toggle() {
            const format = formatField.value;

            // Revert to the plain <textarea>
            if (currentEditor.markdown.container) {
                currentEditor.markdown.container.parentNode.insertBefore(contentField, currentEditor.markdown.container);
                contentField.removeAttribute("style");

                currentEditor.markdown.container.remove();

                currentEditor.markdown.container = null;
                currentEditor.markdown.toolbar   = null;
                currentEditor.markdown.editor    = null;
            } else if (currentEditor.html) {
                currentEditor.html.destroy();
                currentEditor.html = null;
            }
            
            // Create richt-text editor for the chosen format
            if (format === "markdown") {
                currentEditor.markdown.container = document.createElement("div");
                currentEditor.markdown.container.classList.add("wysiwyg_container");

                currentEditor.markdown.toolbar = document.createElement("div");

                currentEditor.markdown.container.appendChild(currentEditor.markdown.toolbar);
                contentField.parentNode.insertBefore(currentEditor.markdown.container, contentField);
                currentEditor.markdown.container.appendChild(contentField);

                currentEditor.markdown.editor = new TinyMDE.Editor({textarea: contentField});

                new TinyMDE.CommandBar({
                    element: currentEditor.markdown.toolbar,
                    editor:  currentEditor.markdown.editor,

                    // TODO: _italic_, more headings?
                    commands: [
                        'bold', 'italic', 'strikethrough', '|',
                        'code', '|',
                        'h1', 'h2', '|',
                        'ul', 'ol', '|',
                        'blockquote', 'hr', '|',
                        'insertLink', 'insertImage'
                    ],
                });
            } else if (format === "html") {
                currentEditor.html = await ckeditor.ClassicEditor.create(contentField, {
                    plugins: [
                        // Basic HTML
                        ckeditor.Essentials,
                        ckeditor.SourceEditing,
                        ckeditor.GeneralHtmlSupport,
                        ckeditor.HtmlEmbed,
                        ckeditor.Autoformat,
                        ckeditor.RemoveFormat,
                        ckeditor.ShowBlocks,

                        ckeditor.BlockQuote,
                        ckeditor.Bold,
                        ckeditor.Heading,
                        ckeditor.Indent,
                        ckeditor.Italic,
                        ckeditor.Highlight,
                        ckeditor.AutoLink,
                        ckeditor.Link,
                        ckeditor.List,
                        ckeditor.Paragraph,
                        ckeditor.Indent,
                        ckeditor.IndentBlock,
                        ckeditor.CodeBlock,
                        ckeditor.Underline,
                        ckeditor.Strikethrough,
                        ckeditor.Code,
                        ckeditor.TodoList,
                        ckeditor.Superscript,
                        ckeditor.Subscript,
                        ckeditor.Alignment,
                        ckeditor.HorizontalLine,
                        ckeditor.SpecialCharacters,
                        ckeditor.SpecialCharactersEssentials,

                        // Embedded Media
                        ckeditor.MediaEmbed,

                        // Images
                        ckeditor.Image,
                        ckeditor.ImageCaption,
                        ckeditor.ImageStyle,
                        ckeditor.ImageToolbar,
                        ckeditor.ImageCaption,
                        ckeditor.ImageBlockEditing,
                        ckeditor.LinkImage,
                        ckeditor.PictureEditing,
                        ckeditor.ImageInsert,
                        ckeditor.ImageResize,
                        ckeditor.AutoImage,

                        // Tables
                        ckeditor.Table,
                        ckeditor.TableToolbar,
                        ckeditor.TableCellProperties,
                        ckeditor.TableProperties,

                        // Copy&Paste from external programs,
                        ckeditor.Clipboard,
                        ckeditor.PasteFromOffice,
                        ckeditor.PasteFromMarkdownExperimental,
                    ],
                    toolbar: {
                        items: [
                            "heading", "showBlocks", "|",
                            "bold", "italic", "underline", "strikethrough", "subscript", "superscript", "code", "alignment", "highlight", "removeFormat", "|",
                            "link", /* "insertImage", */ "insertTable", "blockQuote", "mediaEmbed", "codeBlock", "horizontalLine",  "specialCharacters", "|",
                            "bulletedList", "numberedList", "outdent", "indent", "|",
                            "undo", "redo", "htmlEmbed", "sourceEditing"
                            ],
                        // shouldNotGroupWhenFull: true
                    },
                    table: {
                        contentToolbar: [
                            "tableColumn", "tableRow", "mergeTableCells",
                            "tableProperties", "tableCellProperties"
                        ]
                    },
                    image: {
                        toolbar: [
                            "linkImage",
                            "|",
                            "imageStyle:block",
                            "imageStyle:wrapText",
                            "|",
                            "imageTextAlternative",
                            "toggleImageCaption",
                        ]
                    },
                    htmlSupport: {
                        allow: [
                            {
                                name: /.*/,
                                attributes: true,
                                classes: true,
                                styles: true
                            }
                        ],
                        disallow: [],
                    },
                });
            }
        }

        formatField.addEventListener("change", async () => await toggle());
        await toggle();
    }

    // Handle ...TInline (inline form with formatted content)
    window.setTimeout(async function() {
        const inlineForms = document.querySelectorAll('.dynamic-translations');
    
        for (let inlineForm of inlineForms || []) {
            await toggleContentEditor(inlineForm);
        }
    
        document.addEventListener('formset:added', async function(event) {
            if (!event.target.classList.contains("dynamic-translations")) return;
            await toggleContentEditor(event.target);
        });
    }, 100);
});