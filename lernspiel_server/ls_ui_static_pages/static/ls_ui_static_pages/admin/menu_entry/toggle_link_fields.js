/**
 * Toggle visibility of the link fields depending on the currently chosen link type.
 * Initially or of the link type is "none", no fields will be shown. For all other
 * types only the relevant fields will be shown.
 */
document.addEventListener("DOMContentLoaded", function() {
    const linkTypeField  = document.querySelector("#id_link_type");
    const linkUrlField   = document.querySelector("#id_link_url").closest(".form-row");
    const linkPageField  = document.querySelector("#id_link_page").closest(".form-row");
    const linkViewFields = document.querySelectorAll(".link_view");
    const newWindow      = document.querySelector("#id_new_window").closest(".form-row");

    function toggleFields() {
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

    linkTypeField.addEventListener("change", toggleFields);
    toggleFields();
});
