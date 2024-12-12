document.addEventListener('DOMContentLoaded', () => {
    send_query();
});

function toggleSections() {
    const section1 = document.getElementById('normal-search');
    const section2 = document.getElementById('advanced-search');

    if (section1.style.display === 'block') {
        clearFilters();
        section1.style.display = 'none';
        section2.style.display = 'block';
    } else {
        clearFilters();
        section1.style.display = 'block';
        section2.style.display = 'none';
    }
}

function send_query() {

    console.log("send query...")

    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";
    console.log("hide not found icon");

    const filters = document.querySelectorAll('#filters input, #filters select, #filters [type="radio"], #filters number');

    filters.forEach(filter => {
        filter.addEventListener('input', () => {
            const csrfToken = document.getElementById('csrf_token').value;

            const maxSizeInput = document.querySelector('#query-max-size').value;
            const sizeUnit = document.getElementById('size-unit').value;
            const sizeValue = parseFloat(maxSizeInput);
            let sizeInBytes;

            switch (sizeUnit) {
                case 'kb':
                    sizeInBytes = sizeValue * 1024;
                    break;
                case 'mb':
                    sizeInBytes = sizeValue * 1024 * 1024;
                    break;
                case 'gb':
                    sizeInBytes = sizeValue * 1024 * 1024 * 1024;
                    break;
                default:
                    sizeInBytes = sizeValue;
            }


            const searchCriteria = {
                csrf_token: csrfToken,
                query: document.querySelector('#query').value,
                title: document.querySelector('#query-title').value,
                description: document.querySelector('#query-description').value,
                authors: document.querySelector('#query-authors').value,
                q_tags: document.querySelector('#query-tags').value,
                bytes: sizeInBytes,
                publication_type: document.querySelector('#publication_type').value
            };

            console.log(document.querySelector('#publication_type').value);

            fetch('/exploreuvl', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchCriteria),
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    document.getElementById('results').innerHTML = '';

                    // results counter
                    const resultCount = data.length;
                    const resultText = resultCount === 1 ? 'Model' : 'Models';
                    document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

                    if (resultCount === 0) {
                        console.log("show not found icon");
                        document.getElementById("results_not_found").style.display = "block";
                    } else {
                        document.getElementById("results_not_found").style.display = "none";
                    }


                    data.forEach(dataset => {
                        let card = document.createElement('div');
                        card.className = 'col-12';
                        card.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <div class="d-flex align-items-center justify-content-between">
                                        <h3>${dataset.title}</h3>
                                        <div>
                                            <span class="badge bg-primary" style="cursor: pointer;" onclick="set_publication_type_as_query('${dataset.publication_type}')">${dataset.publication_type}</span>
                                        </div>
                                    </div>

                                    <div class="row mb-2">

                                        <div class="col-md-4 col-12">
                                            <span class=" text-secondary">
                                                Description
                                            </span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            <p class="card-text">${dataset.description}</p>
                                        </div>

                                    </div>

                                    <div class="row mb-2">

                                        <div class="col-md-4 col-12">
                                            <span class=" text-secondary">
                                                Authors
                                            </span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            ${dataset.authors.map(author => `
                                                <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                            `).join('')}
                                        </div>

                                    </div>

                                    <div class="row mb-2">

                                        <div class="col-md-4 col-12">
                                            <span class=" text-secondary">
                                                Tags
                                            </span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                                        </div>

                                    </div>

                                    <div class="row">

                                        <div class="col-md-4 col-12">

                                        </div>
                                        <div class="col-md-8 col-12">
                                            <a class="btn btn-outline-primary btn-sm" href="${dataset.files[0].url}">
                                                Download ${dataset.files.length} files (${get_total_size(dataset.files)} bytes)
                                            </a>
                                            
                                        </div>


                                    </div>

                                </div>
                            </div>
                        `;

                        document.getElementById('results').appendChild(card);
                    });
                });
        });
    });
}

function get_total_size(files) {
    return files.reduce((acc, file) => acc + file.size_in_bytes, 0);

}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('query');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', { bubbles: true }));
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            // Set the value of the select to the value of the matching option
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    publicationTypeSelect.dispatchEvent(new Event('input', { bubbles: true }));
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {

    // Reset the search query
    let queryInput = document.querySelector('#query');
    let queryTitle = document.querySelector('#query-title');
    let queryAuthors = document.querySelector('#query-authors');
    let queryTags = document.querySelector('#query-tags');
    let queryDescription = document.querySelector('#query-description');
    let queryBytes = document.querySelector('#query-max-size');
    queryTitle.value = "";
    queryAuthors.value = "";
    queryTags.value = "";
    queryDescription.value = "";
    queryInput.value = "";
    queryBytes.value = "";

    // queryInput.dispatchEvent(new Event('input', {bubbles: true}));

    // Reset the publication type to its default value
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any"; // replace "any" with whatever your default value is
    // publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));

    // // Reset the sorting option
    // let sortingOptions = document.querySelectorAll('[name="sorting"]');
    // sortingOptions.forEach(option => {
    //     option.checked = option.value == "newest"; // replace "default" with whatever your default value is
    //     // option.dispatchEvent(new Event('input', {bubbles: true}));
    // });

    // Perform a new search with the reset filters
    queryInput.dispatchEvent(new Event('input', { bubbles: true }));
}


document.addEventListener('DOMContentLoaded', () => {

    //let queryInput = document.querySelector('#query');
    //queryInput.dispatchEvent(new Event('input', {bubbles: true}));

    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (queryParam && queryParam.trim() !== '') {

        const queryInput = document.getElementById('query');
        queryInput.value = queryParam
        queryInput.dispatchEvent(new Event('input', { bubbles: true }));
        console.log("throw event");

    } else {
        const queryInput = document.getElementById('query');
        queryInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

});