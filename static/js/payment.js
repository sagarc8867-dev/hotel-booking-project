document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.pay-tab');
    const panels = document.querySelectorAll('.pay-panel');
    const hiddenField = document.getElementById('id_payment_method');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            const target = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            panels.forEach(function (panel) {
                panel.classList.toggle('hidden', panel.dataset.panel !== target);
            });

            if (hiddenField) {
                hiddenField.value = target;
            }

            syncRequiredFields();
        });
    });

    function syncRequiredFields() {
        document.querySelectorAll('.pay-panel').forEach(function (panel) {
            const isVisible = !panel.classList.contains('hidden');
            panel.querySelectorAll('input, select').forEach(function (field) {
                if (field.hasAttribute('data-required-in-panel')) {
                    field.required = isVisible;
                }
            });
        });
    }

    // Run once on load, so the initially-active tab's fields are correctly required
    syncRequiredFields();

    // Auto-format card number with spaces
    const cardField = document.querySelector('.card-field');
    if (cardField) {
        cardField.addEventListener('input', function () {
            let v = cardField.value.replace(/\D/g, '').slice(0, 16);
            cardField.value = v.replace(/(.{4})/g, '$1 ').trim();
        });
    }
});