# Generated manually to add missing columns

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0001_initial'),
    ]

    operations = [
        # Agregar columnas que faltan en la BD
        migrations.RunSQL(
            sql="""
            ALTER TABLE proveedor 
            ADD COLUMN IF NOT EXISTS es_entidad VARCHAR(10) DEFAULT 'false',
            ADD COLUMN IF NOT EXISTS es_grupo VARCHAR(10) DEFAULT 'false',
            ADD COLUMN IF NOT EXISTS esta_activa VARCHAR(10) DEFAULT 'true',
            ADD COLUMN IF NOT EXISTS espyme VARCHAR(10) DEFAULT 'false',
            ADD COLUMN IF NOT EXISTS fecha_creacion DATE NULL,
            ADD COLUMN IF NOT EXISTS codigo_categoria_principal VARCHAR(100) DEFAULT '',
            ADD COLUMN IF NOT EXISTS descripcion_categoria_principal TEXT DEFAULT '',
            ADD COLUMN IF NOT EXISTS fax VARCHAR(50) DEFAULT '',
            ADD COLUMN IF NOT EXISTS sitio_web VARCHAR(500) DEFAULT '',
            ADD COLUMN IF NOT EXISTS pais VARCHAR(100) DEFAULT '',
            ADD COLUMN IF NOT EXISTS departamento VARCHAR(100) DEFAULT '',
            ADD COLUMN IF NOT EXISTS municipio VARCHAR(100) DEFAULT '',
            ADD COLUMN IF NOT EXISTS ubicacion TEXT DEFAULT '',
            ADD COLUMN IF NOT EXISTS nombre_representante_legal VARCHAR(255) DEFAULT '',
            ADD COLUMN IF NOT EXISTS tipo_doc_representante_legal VARCHAR(50) DEFAULT '',
            ADD COLUMN IF NOT EXISTS n_mero_doc_representante_legal VARCHAR(50) DEFAULT '',
            ADD COLUMN IF NOT EXISTS telefono_representante_legal VARCHAR(50) DEFAULT '',
            ADD COLUMN IF NOT EXISTS correo_representante_legal VARCHAR(255) DEFAULT '',
            ADD COLUMN IF NOT EXISTS camaras_comercio TEXT DEFAULT '',
            ADD COLUMN IF NOT EXISTS lista_restrictiva VARCHAR(10) DEFAULT '',
            ADD COLUMN IF NOT EXISTS inhabilidades TEXT DEFAULT '',
            ADD COLUMN IF NOT EXISTS clasificacion_organica VARCHAR(100) DEFAULT '';
            """,
            reverse_sql="""
            ALTER TABLE proveedor 
            DROP COLUMN IF EXISTS es_entidad,
            DROP COLUMN IF EXISTS es_grupo,
            DROP COLUMN IF EXISTS esta_activa,
            DROP COLUMN IF EXISTS espyme,
            DROP COLUMN IF EXISTS fecha_creacion,
            DROP COLUMN IF EXISTS codigo_categoria_principal,
            DROP COLUMN IF EXISTS descripcion_categoria_principal,
            DROP COLUMN IF EXISTS fax,
            DROP COLUMN IF EXISTS sitio_web,
            DROP COLUMN IF EXISTS pais,
            DROP COLUMN IF EXISTS departamento,
            DROP COLUMN IF EXISTS municipio,
            DROP COLUMN IF EXISTS ubicacion,
            DROP COLUMN IF EXISTS nombre_representante_legal,
            DROP COLUMN IF EXISTS tipo_doc_representante_legal,
            DROP COLUMN IF EXISTS n_mero_doc_representante_legal,
            DROP COLUMN IF EXISTS telefono_representante_legal,
            DROP COLUMN IF EXISTS correo_representante_legal,
            DROP COLUMN IF EXISTS camaras_comercio,
            DROP COLUMN IF EXISTS lista_restrictiva,
            DROP COLUMN IF EXISTS inhabilidades,
            DROP COLUMN IF EXISTS clasificacion_organica;
            """
        ),
    ]
