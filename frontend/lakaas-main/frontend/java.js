document.addEventListener("DOMContentLoaded", () => {
    const propertyList = document.getElementById("property-list");
    const propertyForm = document.getElementById("property-form");
    const popup = document.getElementById("popup");
    const popupName = document.getElementById("popup-name");
    const popupPhone = document.getElementById("popup-phone");
    const popupEmail = document.getElementById("popup-email");
    const closePopupButton = document.getElementById("close-popup");

 
    propertyForm.addEventListener("submit", (e) => {
        e.preventDefault();

       
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const location = document.getElementById("location").value.trim();
        const price = document.getElementById("price").value.trim();
        const imageUrl = document.getElementById("image-url").value.trim();

       
        if (!name || !email || !phone || !location || !price || !imageUrl) {
            alert("Kérlek, tölts ki minden mezőt!");
            return;
        }

     
        const propertyHTML = `
            <div class="property" data-name="${name}" data-email="${email}" data-phone="${phone}">
                <img src="${imageUrl}" alt="${location}">
                <h3>${location}</h3>
                <p>Ár: ${price} Ft</p>
                <button class="contact-button">Érdekel</button>
            </div>
        `;

      
        propertyList.insertAdjacentHTML("beforeend", propertyHTML);

      
        propertyForm.reset();
    });


    propertyList.addEventListener("click", (e) => {
        if (e.target.classList.contains("contact-button")) {
            const property = e.target.closest(".property");

            if (!property) {
                alert("Nem található az ingatlan adatai!");
                return;
            }

    
            const email = property.dataset.email;
            const subject = `Érdeklődés az ingatlan iránt (${property.querySelector("h3").textContent})`;
            const body = `Tisztelt ${property.dataset.name},Az alábbi ingatlan iránt szeretnék érdeklődni: ${property.querySelector("h3").textContent} ${property.querySelector("p").textContent} Várom visszajelzését.Köszönettel,[Az Ön neve]`;

           
            window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        }
    });
});
