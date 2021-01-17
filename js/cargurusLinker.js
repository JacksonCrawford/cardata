/* FUNCTION DECLARATION*/
let setSelectFieldValue = (selectField, value) => {
    // Starts by creating an all uppercase version of the value for case-blind comparison
    let comparisonValue = value.toUpperCase()
    Array.from(selectField.options).forEach((option) => {
        // Checks if the inner text of the option is equal to the provided value
        if (option.innerText.toUpperCase() === comparisonValue) {
            // Selects the found option on the select field
            selectField.selectedIndex = option.index;
            // Triggers a 'change' event on the field, just good practice
            let event = document.createEvent('HTMLEvents');
            event.initEvent('change', true, false);
            selectField.dispatchEvent(event);
        }
    });
}

/* MAIN CODE STARTS HERE */
let { make, model, zip } = arguments[0];
// Grabs the fields for each argument
let makeField = document.getElementById("carPickerUsed_makerSelect");
let modelField = document.getElementById("carPickerUsed_modelSelect");
let zipField = document.getElementById("dealFinderZipUsedId_dealFinderForm");
// Sets the value of the makeField
setSelectFieldValue(makeField, make)
// Sets the value of the modelField
setSelectFieldValue(modelField, model)
// Sets the value of the zipField
zipField.value = zip
// Submits the form to get the URL
let formElement = document.getElementById("dealFinderForm");
formElement.submit()
