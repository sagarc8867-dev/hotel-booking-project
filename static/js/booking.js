document.addEventListener('DOMContentLoaded', function () {
    const idType = document.getElementById('id_id_proof_type');
    const idNumber = document.getElementById('id_id_proof_number');

    if (!idType || !idNumber) return;

    const rules = {
        aadhar:          { maxLength: 12, numericOnly: true,  placeholder: '12-digit Aadhar number' },
        pan:             { maxLength: 10, numericOnly: false, placeholder: 'ABCDE1234F', uppercase: true },
        passport:        { maxLength: 8,  numericOnly: false, placeholder: 'A1234567',   uppercase: true },
        driving_license: { maxLength: 16, numericOnly: false, placeholder: 'e.g. KA0120110012345', uppercase: true },
        voter_id:        { maxLength: 10, numericOnly: false, placeholder: 'ABC1234567', uppercase: true },
    };

    function applyRule() {
        const rule = rules[idType.value];
        idNumber.value = '';
        if (!rule) {
            idNumber.removeAttribute('maxlength');
            idNumber.placeholder = '';
            return;
        }
        idNumber.setAttribute('maxlength', rule.maxLength);
        idNumber.placeholder = rule.placeholder;
    }

    idType.addEventListener('change', applyRule);
    applyRule(); // run once on page load in case a value is already selected

    idNumber.addEventListener('input', function () {
        const rule = rules[idType.value];
        if (!rule) return;

        let value = idNumber.value;
        if (rule.numericOnly) {
            value = value.replace(/\D/g, '');
        }
        if (rule.uppercase) {
            value = value.toUpperCase();
        }
        idNumber.value = value.slice(0, rule.maxLength);
    });
});