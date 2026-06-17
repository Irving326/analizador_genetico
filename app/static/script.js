 async function subirArchivo() {
        const fileInput = document.getElementById('vcfFile');
        const resultadoDiv = document.getElementById('resultado'); 
        const loader = document.getElementById('loader');

        if (fileInput.files.length === 0) {
            alert("Por favor selecciona un archivo primero.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        loader.style.display = "block";
        resultadoDiv.innerHTML = ""; 

        try {
            //  Enviamos la petición y esperamos la respuesta
            const response = await fetch('/analysis/upload-vcf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error en el servidor: ${response.status}`);
            }

            //  Convertimos la respuesta a JSON
            const data = await response.json();

            // Llamamos a la función para crear los datos
            mostrarResultados(data.variantes);

        } catch (error) {
            console.error('Error:', error);
            resultadoDiv.innerText = "Error: No se pudo conectar con el servidor.";
        } finally {
            loader.style.display = "none";
        }
    }

    function mostrarResultados(lista) {
        const resultadoDiv = document.getElementById('resultado');
        
        if (!lista || lista.length === 0) {
            resultadoDiv.innerHTML = '<p style="color: #7f8c8d;">No se encontraron variantes de relevancia médica en este archivo.</p>';
            return;
        }

        
        let html = `
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
                <thead>
                    <tr style="background-color: #000080db; color: white;">
                        <th style="padding: 8px; text-align: left;">Cromosoma</th>
                        <th style="padding: 8px; text-align: left;">Posición</th>
                        <th style="padding: 8px; text-align: left;">Relevancia</th>
                        <th style="padding: 8px; text-align: left;">Enfermedad Asociada</th>
                    </tr>
                </thead>
                <tbody>`;

        lista.forEach(v => {
            html += `
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">${v.chrom}</td>
                    <td style="padding: 8px;">${v.pos}</td>
                    <td style="padding: 8px; color: #e74c3c; font-weight: bold;">${v.relevancia}</td>
                    <td style="padding: 8px;">${v.enfermedad}</td>
                </tr>`;
        });

        html += '</tbody></table>';
        resultadoDiv.innerHTML = html;
    }

    async function buscarVariante (){
        const chrom = document.getElementById("chromosome-list").value;
        const pos = document.getElementById("position").value;
        const ref = document.getElementById("reference").value;
        const alt = document.getElementById("alternative").value;

        const resultadoDiv = document.getElementById('resultado');

        if (!chrom|| !pos || !ref || !alt){
            alert ("Porfavor llena todos los campos para buscar la variante.")
            return;
        }

        const datosVariante = {
            chrom: chrom,
            pos: pos,
            ref: ref,
            alt: alt
        };
        
        
        resultadoDiv.innerHTML = '<p style="color: #7f8c8d;">Consultando base de datos médica...</p>';

        try {
            const response = await fetch('/analysis/search-variant',{
                method:'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datosVariante)
            });
            if (!response.ok) {
            // Leemos el mensaje de error detallado que nos manda FastAPI
            const errorDetalle = await response.json(); 
            console.error("Detalles exactos del error 422:", errorDetalle);
            throw new Error(`Error en el servidor: ${response.status}`);
        }
            const data = await response.json();

            mostrarResultados(data.variantes);
        }catch (error) {
            console.error('Error:', error);
            resultadoDiv.innerHTML = "<p style='color: red;'>Error al buscar la variante individual.</p>";
        }
    }