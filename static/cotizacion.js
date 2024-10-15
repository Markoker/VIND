function updateForm(){
    const tipo = document.getElementById("id_tipo").value;
    const monto = document.getElementById("id_monto").value;

    document.getElementById("solo_traslado").style.display = "none";
    document.getElementById("solo_colacion").style.display = "none";
    document.getElementById("traslado_colacion").style.display = "none";

    if(tipo == "solo_traslado"){
        document.getElementById("solo_traslado").style.display = "block";
    }else if (tipo == "solo_colacion"){
        document.getElementById("solo_colacion").style.display = "block";
    }else if (tipo == "Traslado y colacion"){
        document.getElementById("solo_traslado").style.display = "block";
        document.getElementById("solo_colacion").style.display = "block";
    }

    if(monto > 1000000){
        document.getElementById("cotizaciones").style.display = "block";
    }else{
        document.getElementById("cotizacion").style.display = "none";
    }
}