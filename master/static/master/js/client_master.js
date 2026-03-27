
var ClientMaster = function () {
    var config = {
        submissionUrl: '/master/clientMaster/create',
        successRedirectUrl: '/master/clientMaster/list',
        isUpdate: false,
        method: 'POST',
        storageKey: 'clientMasterFormData'
    };

    var init = function (userConfig) {
        $.extend(config, userConfig);

        // Enhance storage key with referenceId if provided (for updates)
        if (config.referenceId) {
            config.storageKey = 'clientMasterFormData_' + config.referenceId;
        }

        handleNavigation();
        handleSubmission();
        handleAddressSync();
        loadFromLocalStorage();
        handleInputPersistence();
    };

    var handleInputPersistence = function () {
        $('input, select, textarea').on('input change', function () {
            saveToLocalStorage();
        });
    };

    var saveToLocalStorage = function () {
        var formData = {};
        $('input, select, textarea').each(function () {
            var name = $(this).attr('name');
            if (name) {
                if ($(this).attr('type') === 'checkbox') {
                    formData[name] = $(this).is(':checked');
                } else if ($(this).attr('type') !== 'file' && $(this).attr('type') !== 'password') {
                    formData[name] = $(this).val();
                }
            }
        });

        var storageData = {
            timestamp: new Date().getTime(),
            data: formData
        };

        localStorage.setItem(config.storageKey, JSON.stringify(storageData));
    };

    var loadFromLocalStorage = function () {
        var savedString = localStorage.getItem(config.storageKey);
        if (savedString) {
            try {
                var storageData = JSON.parse(savedString);

                // Expiration check: 24 hours (24 * 60 * 60 * 1000 ms)
                var now = new Date().getTime();
                var expirationTime = 24 * 60 * 60 * 1000;

                if (now - storageData.timestamp > expirationTime) {
                    console.log("Draft expired, removing.");
                    localStorage.removeItem(config.storageKey);
                    return;
                }

                var formData = storageData.data;
                $.each(formData, function (name, value) {
                    var element = $('[name="' + name + '"]');
                    if (element.length > 0) {
                        if (element.attr('type') === 'checkbox') {
                            element.prop('checked', value).trigger('change');
                        } else if (element.hasClass('select2')) {
                            element.val(value).trigger('change');
                        } else {
                            element.val(value);
                        }
                    }
                });

                if (formData && Object.keys(formData).length > 0) {
                    toastr.info('Continuing from previously unsaved draft.');
                }
            } catch (e) {
                console.error("Error parsing saved data", e);
            }
        }

        // Cleanup old drafts from other clients periodically
        cleanupOldDrafts();
    };

    var cleanupOldDrafts = function () {
        var now = new Date().getTime();
        var expirationTime = 7 * 24 * 60 * 60 * 1000; // 7 days for cleanup

        for (var i = 0; i < localStorage.length; i++) {
            var key = localStorage.key(i);
            if (key.startsWith('clientMasterFormData')) {
                try {
                    var data = JSON.parse(localStorage.getItem(key));
                    if (data.timestamp && (now - data.timestamp > expirationTime)) {
                        localStorage.removeItem(key);
                    }
                } catch (e) { }
            }
        }
    };

    var handleAddressSync = function () {
        $('#clientMasterIsTemporaryAddressSameAsPermanentAddress').on('change', function () {
            if ($(this).is(':checked')) {
                $('#clientMasterTemporaryMunicipality').val($('#clientMasterPermanentMunicipality').val()).trigger('change');
                $('#clientMasterTemporaryDistrict').val($('#clientMasterPermanentDistrict').val()).trigger('change');
                $('#clientMasterTemporaryProvince').val($('#clientMasterPermanentProvince').val()).trigger('change');
                $('#clientMasterTemporaryWardNo').val($('#clientMasterPermanentWardNo').val());
                $('#clientMasterTemporaryStreet').val($('#clientMasterPermanentStreet').val());
            } else {
                // Only clear if we're unchecking, but loadFromLocalStorage might have set it.
                // However, handleAddressSync is usually for manual toggling.
            }
            saveToLocalStorage();
        });
    };

    var handleNavigation = function () {
        // Next Button
        $('.client-master-next-btn').on('click', function () {
            var currentTab = $('.tab-pane.active');
            var nextTab = currentTab.next('.tab-pane');

            if (validateTab(currentTab)) {
                if (nextTab.length > 0) {
                    var nextTabId = nextTab.attr('id');
                    $('a[href="#' + nextTabId + '"]').tab('show');
                }
            }
        });

        // Previous Button
        $('.client-master-prev-btn').on('click', function () {
            var currentTab = $('.tab-pane.active');
            var prevTab = currentTab.prev('.tab-pane');

            if (prevTab.length > 0) {
                var prevTabId = prevTab.attr('id');
                $('a[href="#' + prevTabId + '"]').tab('show');
            }
        });

        // Handle tab clicks directly
        $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
            var currentTab = $('.tab-pane.active');
            var targetTab = $($(e.target).attr('href'));

            // Only validate if we are going forward? Or always?
            // For better UX, let's always validate the current tab before allowing switch.
            if (!validateTab(currentTab)) {
                e.preventDefault();
            }
        });
    };

    var validateTab = function (tab) {
        var isValid = true;

        // Remove existing error states
        tab.find('.is-invalid').removeClass('is-invalid');
        tab.find('.invalid-feedback').remove();

        tab.find('input[required], select[required], textarea[required]').each(function () {
            var element = $(this);
            if (element.val() === '' || element.val() === null) {
                element.addClass('is-invalid');

                // Add error message if not present
                if (element.parent().find('.invalid-feedback').length === 0) {
                    element.after('<div class="invalid-feedback">This field is required.</div>');
                }
                isValid = false;
            }
        });

        if (!isValid) {
            // Optional: Toast message
            if (typeof Toast !== 'undefined') {
                Toast.fire({
                    icon: 'error',
                    title: 'Please fill all mandatory fields.'
                });
            } else {
                alert('Please fill all mandatory fields correctly.');
            }
        }

        return isValid;
    };

    var handleSubmission = function () {
        $('#btnSaveClientMaster').on('click', function () {
            // Validate all tabs before submission
            var allTabsValid = true;
            $('.tab-pane').each(function () {
                if (!validateTab($(this))) {
                    allTabsValid = false;
                    // Show the first invalid tab
                    var tabId = $(this).attr('id');
                    $('a[href="#' + tabId + '"]').tab('show');
                    return false; // Break loop
                }
            });

            if (!allTabsValid) return;

            var formData = {};
            $('input, select, textarea').each(function () {
                var name = $(this).attr('name');
                if (name) {
                    if ($(this).attr('type') === 'checkbox') {
                        formData[name] = $(this).is(':checked');
                    } else if ($(this).attr('type') !== 'file') {
                        formData[name] = $(this).val();
                    }
                }
            });

            const inputJson = JSON.stringify(formData);

            openConfirmSaveModal(inputJson, 'clientMasterForm', saveClientData, config.submissionUrl, config.successRedirectUrl);
        });
    };

    function saveClientData(inputJson, formId, requestUrl, redirectUrl) {
        $.ajax({
            url: requestUrl,
            type: config.method,
            data: inputJson,
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('#' + formId).find('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.status === 'success' || response.resultCode === '0') {
                    localStorage.removeItem(config.storageKey);
                    toastrSuccessMessage(config.isUpdate ? 'Client updated successfully!' : 'Client created successfully!');
                    setTimeout(function () {
                        window.location.href = redirectUrl;
                    }, 500);
                } else {
                    toastrErrorMessage('Error: ' + JSON.stringify(response.message || response.response || response.resultDescription));
                    console.error(response);
                }
            },
            error: function (xhr, status, error) {
                toastrErrorMessage('An error occurred: ' + error);
                console.error(xhr.responseText);
            }
        });
    }

    // Helper to get CSRF token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    return {
        init: init
    };
}();
