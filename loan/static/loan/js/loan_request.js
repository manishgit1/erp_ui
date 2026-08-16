
var loanRequestsList = [];

$(document).ready(function () {
    handleNavigation();
    initDynamicSections();
});

function handleNavigation() {
    // Next Button
    $('.loan-request-next-btn').on('click', function () {
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
    $('.loan-request-prev-btn').on('click', function () {
        var currentTab = $('.tab-pane.active');
        var prevTab = currentTab.prev('.tab-pane');

        if (prevTab.length > 0) {
            var prevTabId = prevTab.attr('id');
            $('a[href="#' + prevTabId + '"]').tab('show');
        }
    });
}

function validateTab(tab) {
    var isValid = true;
    tab.find('input[required], select[required]').each(function () {
        if ($(this).val() === '') {
            $(this).addClass('is-invalid');
            isValid = false;
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    return isValid;
}

function initDynamicSections() {
    // Collateral
    $('#btnAddCollateral').on('click', function () {
        var uniqueId = Date.now();
        var html = `
            <div class="card mb-3 collateral-item" id="collateral_${uniqueId}">
                <div class="card-body">
                    <h6 class="card-title">Collateral Item</h6>
                    <button type="button" class="close float-right remove-section" data-target="#collateral_${uniqueId}">&times;</button>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Collateral Type</label>
                                <input type="text" class="form-control form-control-sm" name="collateralType[]">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Valuation Amount</label>
                                <input type="number" class="form-control form-control-sm" name="collateralValue[]">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        $('#collateralList').append(html);
    });

    // Guarantors
    $('#btnAddGuarantor').on('click', function () {
        var uniqueId = Date.now();
        var html = `
            <div class="card mb-3 guarantor-item" id="guarantor_${uniqueId}">
                <div class="card-body">
                    <h6 class="card-title">Guarantor</h6>
                    <button type="button" class="close float-right remove-section" data-target="#guarantor_${uniqueId}">&times;</button>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Guarantor Name</label>
                                <input type="text" class="form-control form-control-sm" name="guarantorName[]">
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label>Contact Number</label>
                                <input type="text" class="form-control form-control-sm" name="guarantorContact[]">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        $('#guarantorList').append(html);
    });

    // Remove Section
    $(document).on('click', '.remove-section', function () {
        $($(this).data('target')).remove();
    });


    $('#btnSaveLoanRequest').off('click').on('click', function () {
        var form = $("#loanRequestForm");

        var rules = {
            loanRequestAmount: {
                required: true
            },
            loanRequestTenure: {
                required: true
            },
            loanRequestPurpose: {
                required: true
            },
            loanRequestInterestRate: {
                required: true
            },
            loanRequestType: {
                required: true
            },
            loanRequestPaymentScheme: {
                required: true
            }

        }

        // if (!validateForm("#contactMasterForm", rules)) {
        //     return; 
        // }

        var inputJson = JSON.stringify(convertToJsonForLoanRequest());


        openConfirmSaveModal(inputJson, 'loanRequestForm', saveInsertUpdateData, LOAN_REQUEST_CREATE_URL, LOAN_REQUEST_LIST_URL);

    })
}



function convertToJsonForLoanRequest() {
    var loanRequestData = {};
    loanRequestData.loanRequestDateAd = $('#loanRequestValueDate').val();
    loanRequestData.loanRequestAmount = $('#loanRequestAmount').val();
    loanRequestData.loanRequestTenure = $('#loanRequestTenure').val();
    loanRequestData.loanRequestPurpose = $('#loanRequestPurpose').val();
    loanRequestData.loanRequestInterestRate = $('#loanRequestInterestRate').val();
    loanRequestData.loanRequestType = $('#loanRequestType').val();
    loanRequestData.loanRequestPaymentScheme = $('#loanRequestPaymentScheme').val();

    loanRequestData.loanRequestMobileNumber = $('#loanRequestClientMobileNumber').val();
    loanRequestData.loanRequestClientCode = $('#loanRequestClientCode').val();

    loanRequestData.collateral = getCollateralData();
    loanRequestData.guarantors = getGuarantorData();

    return loanRequestData;
}

function getCollateralData() {
    var collateralData = [];
    $('.collateral-item').each(function () {
        var item = {};
        item.collateralType = $(this).find('input[name="collateralType[]"]').val();
        item.collateralValue = $(this).find('input[name="collateralValue[]"]').val();
        collateralData.push(item);
    });
    return collateralData;
}

function getGuarantorData() {
    var guarantorData = [];
    $('.guarantor-item').each(function () {
        var item = {};
        item.guarantorName = $(this).find('input[name="guarantorName[]"]').val();
        item.guarantorContact = $(this).find('input[name="guarantorContact[]"]').val();
        guarantorData.push(item);
    });
    return guarantorData;
}

var loanRequestsData = {};

function loadLoanRequestList(requestUrl, tableId) {
    $.ajax({
        url: requestUrl,
        method: "GET",
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            var tbody = $('#' + tableId + ' tbody');
            tbody.empty();
            var datas = [];
            if (data.datas) {
                datas = data.datas;
            } else if (data.data) {
                datas = data.data;
            } else if (Array.isArray(data)) {
                datas = data;
            } else if (data.response && Array.isArray(data.response)) {
                datas = data.response;
            }

            loanRequestsData[tableId] = datas;

            var approveButtonText = tableId === 'approvedLoanTable' ? 'Disburse' : 'Forward';
            if (datas && datas.length > 0) {
                datas.forEach(function (item, index) {
                    var refId = item.referenceId || item.id || '';
                    var tr = `
                        <tr>
                            <td>${item.clientName || item.customerName || ''}</td>
                            <td>${item.clientCode || ''}</td>
                            <td>${item.mobileNumber || item.clientMobileNumber || ''}</td>
                            <td>${formatCurrency(item.loanAmount || item.amount || 0)}</td>
                            <td>${item.tenureMonths || item.loanTenure || item.tenure || ''}</td>
                            <td>${item.interestRate || item.loanInterestRate || ''}%</td>
                            <td>${item.loanPurpose || item.purpose || item.loanType || ''}</td>
                            <td><span class="badge badge-info">${item.status || 'Pending'}</span></td>
                            <td>
                                <div style="display: flex; gap: 5px;">
                                    <button type="button" class="btn btn-xs btn-outline-primary" onclick="viewLoanRequest('${refId}')" title="View"><i class="fas fa-eye"></i></button>
                                    
                                    ${(item.canApprove || item.isApprovable) ? `
                                        ${approveButtonText === 'Disburse' ? `
                                            <button type="button" class="btn btn-xs btn-success" onclick="openDisbursementPage('${refId}')" title="${approveButtonText}">${approveButtonText}</button>
                                        ` : `
                                            <button type="button" class="btn btn-xs btn-success" onclick="openLoanActionModal(${index}, '${tableId}', 'APPROVE')" title="${approveButtonText}">${approveButtonText}</button>
                                        `}
                                        <button type="button" class="btn btn-xs btn-danger" onclick="openLoanActionModal(${index}, '${tableId}', 'REJECT')" title="Reject">Reject</button>
                                    ` : ''}

                                    ${(item.canEdit || item.isEditable) ? `
                                        <button type="button" class="btn btn-xs btn-warning" onclick="editLoanRequest('${refId}')" title="Edit"><i class="fas fa-edit"></i></button>
                                    ` : ''}

                                    ${(item.canRevert || item.isRevertible) ? `
                                        <button type="button" class="btn btn-xs btn-secondary" onclick="openLoanActionModal(${index}, '${tableId}', 'REVERT')" title="Revert">Revert</button>
                                    ` : ''}
                                    
                                    <button type="button" class="btn btn-xs btn-outline-info" onclick="timelineData('${refId}')" title="Timeline"><i class="fas fa-history"></i></button>

                                    <button type="button" class="btn btn-xs btn-outline-info" onclick='printLoanRequest(${index}, "${tableId}")' title="Print"><i class="fas fa-print"></i></button>
                                </div>
                            </td>
                        </tr>
                    `;
                    tbody.append(tr);
                });
            } else {
                tbody.append('<tr><td colspan="9" class="text-center">No loan requests found.</td></tr>');
            }
        },
        error: function (jqXHR, textStatus, errorMessage) {
            console.error('Error loading loan requests for ' + tableId + ':', errorMessage);
        }
    });
}


function printLoanRequest(index, tableId) {
    var d = loanRequestsData[tableId] ? loanRequestsData[tableId][index] : null;
    if (!d) return;


    // debugger

    // var d = JSON.parse(data);
    // debugger

    function formatDate(dateStr) {
        if (!dateStr) return '';
        var d = new Date(dateStr);
        return d.toLocaleDateString('en-GB');
    }

    var html = `
    <html>
    <head>
        <title>Loan Request</title>
        <style>

        body{
            font-family: Arial, sans-serif;
            padding:40px;
            color:#000;
        }

        h2{
            text-align:center;
            margin-bottom:30px;
        }

        table{
            width:100%;
            border-collapse:collapse;
            margin-bottom:20px;
        }

        td,th{
            padding:8px;
            border:1px solid #000;
            font-size:14px;
        }

        .section-title{
            background:#f2f2f2;
            font-weight:bold;
            text-align:left;
        }

        .sign-area{
            margin-top:80px;
            width:100%;
        }

        .sign-area td{
            border:none;
            text-align:center;
            padding-top:50px;
        }

        </style>
    </head>

    <body>

        <h2>Loan Request</h2>

        <table>
            <tr>
                <th colspan="4" class="section-title">Customer Information</th>
            </tr>

            <tr>
                <td><b>Client Name</b></td>
                <td>${d.clientName || d.customerName || ''}</td>
                <td><b>Client Code</b></td>
                <td>${d.clientCode || ''}</td>
            </tr>

            <tr>
                <td><b>Mobile Number</b></td>
                <td>${d.mobileNumber || d.clientMobileNumber || ''}</td>
                <td><b>Permanent Address</b></td>
                <td>${d.permanentAddress || d.clientPermanentAddress || ''}</td>
            </tr>
        </table>

        <table>
            <tr>
                <th colspan="4" class="section-title">Loan Information</th>
            </tr>

            <tr>
                <td><b>Loan Type</b></td>
                <td>${d.loanType || ''}</td>
                <td><b>Loan Purpose</b></td>
                <td>${d.loanPurpose || d.purpose || ''}</td>
            </tr>

            <tr>
                <td><b>Loan Amount</b></td>
                <td>${formatCurrency(d.loanAmount || d.amount || 0)}</td>
                <td><b>Interest Rate</b></td>
                <td>${d.interestRate || d.loanInterestRate || ''}%</td>
            </tr>

            <tr>
                <td><b>Tenure (Months)</b></td>
                <td>${d.tenureMonths || d.loanTenure || d.tenure || ''}</td>
                <td><b>EMI Date</b></td>
                <td>${formatDate(d.emiDateAd)}</td>
            </tr>
        </table>

        <table>
            <tr>
                <th class="section-title">Remarks</th>
            </tr>
            <tr>
                <td style="height:60px">${d.remarks || ''}</td>
            </tr>
        </table>

        <table class="sign-area">
            <tr>
                <td>______________________</td>
                <td>______________________</td>
                <td>______________________</td>
            </tr>
            <tr>
                <td>Customer Signature</td>
                <td>Prepared By</td>
                <td>Approved By</td>
            </tr>
        </table>

    </body>
    </html>
    `;

    var printWindow = window.open('', '', 'width=900,height=700');

    printWindow.document.write(html);
    printWindow.document.close();

    printWindow.focus();
    printWindow.print();
    printWindow.close();
}

function openLoanActionModal(index, tableId, actionType) {
    var d = loanRequestsData[tableId] ? loanRequestsData[tableId][index] : null;
    if (!d) return;

    $('#loanActionRemarks').val('');
    $('#modalClientName').text(d.clientName || d.customerName || '-');
    $('#modalClientAddress').text(d.permanentAddress || d.clientPermanentAddress || '-');
    $('#modalLoanAmount').text(formatCurrency(d.loanAmount || d.amount || 0));
    $('#modalInterestRate').text((d.interestRate || d.loanInterestRate || '0') + '%');

    var modalTitle = '';
    var btnClass = '';
    var btnText = '';
    var isRemarksRequired = false;

    if (actionType === 'APPROVE') {
        modalTitle = 'Approve/Forward Loan Request';
        btnClass = 'btn-success';
        btnText = 'Forward';
    } else if (actionType === 'REJECT') {
        modalTitle = 'Reject Loan Request';
        btnClass = 'btn-danger';
        btnText = 'Reject';
        isRemarksRequired = true;
    } else if (actionType === 'REVERT') {
        modalTitle = 'Revert Loan Request';
        btnClass = 'btn-secondary';
        btnText = 'Revert';
        isRemarksRequired = true;
    }

    $('#loanActionModalTitle').text(modalTitle);
    $('#btnLoanActionSubmit').removeClass('btn-success btn-danger btn-secondary').addClass(btnClass).text(btnText);

    if (isRemarksRequired) {
        $('#remarksRequiredLabel').removeClass('d-none');
    } else {
        $('#remarksRequiredLabel').addClass('d-none');
    }

    $('#loanActionModal').modal('show');

    $('#btnLoanActionSubmit').off('click').on('click', function () {
        var remarks = $('#loanActionRemarks').val().trim();
        if (isRemarksRequired && !remarks) {
            toastrErrorMessage("Remarks are required for this action.");
            return;
        }

        var refId = d.referenceId || d.id || '';
        if (actionType === 'APPROVE') {
            approveLoanRequest(refId, remarks);
        } else if (actionType === 'REJECT') {
            rejectLoanRequest(refId, remarks);
        } else if (actionType === 'REVERT') {
            revertLoanRequest(refId, remarks);
        }
        $('#loanActionModal').modal('hide');
    });
}

function approveLoanRequest(referenceId, remarks) {
    var payload = {
        loanRequestId: referenceId,
        approvalStatus: 'APPROVED',
        remarks: remarks
    };

    ajaxPostRequest('/loan/loanRequest/approve', payload, function (response) {
        toastrSuccessMessage("Loan request approved successfully.");
        location.reload();
    });
}

function rejectLoanRequest(referenceId, remarks) {
    var payload = {
        referenceId: referenceId,
        remarks: remarks
    };

    ajaxPostRequest('/loan/loanRequest/reject', payload, function (response) {
        toastrSuccessMessage("Loan request rejected.");
        location.reload();
    });
}

function revertLoanRequest(referenceId, remarks) {
    var payload = {
        referenceId: referenceId,
        remarks: remarks
    };

    ajaxPostRequest('/loan/loanRequest/revert', payload, function (response) {
        toastrSuccessMessage("Loan request reverted.");
        location.reload();
    });
}

function openDisbursementPage(referenceId) {
    var jsonData = {
        'referenceId': referenceId
    };
    window.location.href = '/loan/loanRequest/disburse?jsonData=' + encodeURIComponent(JSON.stringify(jsonData));
}

function disburseLoanRequest(referenceId, remarks) {
    var payload = {
        loanRequestId: referenceId,
        approvalStatus: 'DISBURSED',
        remarks: remarks
    };

    ajaxPostRequest('/loan/loanRequest/approve', payload, function (response) {
        if (response.resultCode === '0') {
            toastrSuccessMessage("Loan request disbursed successfully.");
            setTimeout(function () {
                window.location.href = LOAN_REQUEST_LIST_URL;
            }, 1000);
        } else {
            toastrErrorMessage(response.resultDescription || "Disbursement failed.");
        }
    });
}

function viewLoanRequest(referenceId) {
    window.location.href = '/loan/loanRequest/view/' + referenceId;
}

function editLoanRequest(referenceId) {
    window.location.href = '/loan/loanRequest/edit/' + referenceId;
}

// Helper for AJAX POST
function ajaxPostRequest(url, data, successCallback) {
    $.ajax({
        url: url,
        method: "POST",
        data: JSON.stringify(data),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: successCallback,
        error: function (xhr) {
            var errorMsg = "An error occurred.";
            try {
                var response = JSON.parse(xhr.responseText);
                errorMsg = response.resultDescription || response.message || errorMsg;
            } catch (e) { }
            toastrErrorMessage(errorMsg);
        }
    });
}

// Global CSRF helper if not already defined
if (typeof getCookie !== 'function') {
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
}




