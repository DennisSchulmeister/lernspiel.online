document.addEventListener("DOMContentLoaded", function() {
    /**
     * Toggle visibility of the link fields depending on the currently chosen link type.
     * Initially or of the link type is "none", no fields will be shown. For all other
     * types only the relevant fields will be shown.
     */
    function toggleFields(container) {
        const linkTypeField  = container.querySelector(".link_type");
        const linkUrlField   = container.querySelector(".link_url").closest(".form-row");
        const linkPageField  = container.querySelector(".link_page").closest(".form-row");
        const linkViewFields = container.querySelectorAll(".link_view");
        const newWindow      = container.querySelector(".new_window").closest(".form-row");
    
        function toggle() {
            const linkType = linkTypeField.value;
            
            linkUrlField.style.display = "none";
            linkPageField.style.display = "none";
            linkViewFields.forEach(field => field.closest(".form-row").style.display = "none");
            newWindow.style.display = "none";
    
            if (linkType === "url") {
                linkUrlField.style.display = "block";
            } else if (linkType === "page") {
                linkPageField.style.display = "block";
            } else if (linkType === "view") {
                linkViewFields.forEach(field => field.closest(".form-row").style.display = "block");
            }
    
            if (linkType && linkType !== "none") {
                newWindow.style.display = "block";
            }
        }
    
        linkTypeField.addEventListener("change", toggle);
        toggle();
    }

    /**
     * Move input fields for the view parameters into a single line so that they take up
     * less vertical space.
     */
    function moveViewParameters(container) {
        const firstRow   = container.querySelector(".field-link_view_par1");
        let currentInput = firstRow.querySelector("input");
        let otherRows = [];

        for (let formRow of container.querySelectorAll(".form-row")) {
            if (formRow.classList.contains("field-link_view_par1")) continue;
            if (!formRow.getAttribute("class").includes("field-link_view_par")) continue;
            otherRows.push(formRow);
        }

        for (let otherRow of otherRows) {
            const inputField = otherRow.querySelector("input");
            currentInput.after(inputField);
            currentInput = inputField;

            otherRow.remove();
        }
    }

    // Handle MenuEntryAdmin (stand-alone page for menu entry)
    const mainForm = document.querySelector("#menuentry_form");
    
    if (mainForm) {
        toggleFields(mainForm);
        moveViewParameters(mainForm);
    }

    // Handle MenuEntryInline (inline form for menu entries)
    window.setTimeout(function() {
        const inlineForms = document.querySelectorAll('.dynamic-menu_entries');
    
        for (let inlineForm of inlineForms || []) {
            toggleFields(inlineForm);
            moveViewParameters(inlineForm);
        }
    
        document.addEventListener('formset:added', function(event) {
            if (!event.target.classList.contains("dynamic-menu_entries")) return;

            toggleFields(event.target);
            moveViewParameters(event.target);
        });
    }, 100);
});
