

document.addEventListener('DOMContentLoaded', () => {
    // Example API call
    fetch('/api/hello?name=User')
        .then(response => response.json())
        .then(data => {
            const element = document.getElementById('api-response');
            if (element) {
                element.textContent = data.message;
            }
        });
});

        const md = window.markdownit();
        var simplemde = null;
        // Function to render Markdown
        function renderMarkdown() {
            const markdownInput = document.getElementById('document-input').value;
            const html = md.render(markdownInput);
            document.getElementById('document-rendered').innerHTML = html;
        }

        function openTab(evt, cityName) {
            // Declare all variables
            var i, tabcontent, tablinks;

            // Get all elements with class="tabcontent" and hide them
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }

            // Get all elements with class="tablinks" and remove the class "active"
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }

            // Show the current tab, and add an "active" class to the button that opened the tab
            document.getElementById(cityName).style.display = "block";
            evt.currentTarget.className += " active";
        }

        function activeAdvanced() {

            if (simplemde == null) {
                simplemde = new SimpleMDE({
                    element: document.getElementById("document-input")
                });
                simplemde.codemirror.on("change", function() {
                    const mdIn = simplemde.value();
                    var ourHtml = md.render(mdIn);
                    document.getElementById('document-rendered').innerHTML = ourHtml;

                });
            }
        }

        function killAdvanced() {
            if (simplemde != null) {
                simplemde.toTextArea();
                simplemde = null;
                document.getElementById('document-input').addEventListener('input', renderMarkdown);

            }
        }


        // Render Markdown on initial load
        document.getElementById('defaultOpen').click();
        renderMarkdown();
        document.getElementById('document-input').addEventListener('input', renderMarkdown);
