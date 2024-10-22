<?php
// Esto configura la base de datos
$servername = "localhost";
$username = "tu_usuario";  
$password = "tu_contraseña"; 
$dbname = "inventario";  
// Crea la conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verifica la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Verifica si se envió el formulario
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $producto_id = $_POST['producto'];
    $cantidad_retirada = $_POST['cantidad'];
    $fecha_salida = $_POST['fecha'];

    // Consulta la cantidad actual del producto
    $sql = "SELECT cantidad FROM productos WHERE id = $producto_id";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $cantidad_actual = $row['cantidad'];

        // Verificar si hay suficiente cantidad
        if ($cantidad_actual >= $cantidad_retirada) {
            // Restar la cantidad retirada
            $nueva_cantidad = $cantidad_actual - $cantidad_retirada;

            // Actualiza la base de datos
            $sql_update = "UPDATE productos SET cantidad = $nueva_cantidad WHERE id = $producto_id";
            if ($conn->query($sql_update) === TRUE) {
                echo "Salida registrada exitosamente. Nueva cantidad: " . $nueva_cantidad;
            } else {
                echo "Error al actualizar el producto: " . $conn->error;
            }
        } else {
            echo "Error: no hay suficiente stock para realizar la salida.";
        }
    } else {
        echo "Producto no encontrado.";
    }
}

// Cierra la conexión
$conn->close();
?>
