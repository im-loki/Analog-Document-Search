package com.fyp.fyp01;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class ocr_engine extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ocr_engine);
    }

    public void ocr_camera(View view) {
//        Toast.makeText(this, "Opening Camera", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(this, ocr_camera.class));
        finish();
    }

    public void ocr_photos(View view) {
//        Toast.makeText(this, "Opening Photos", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(this, ocr_photos.class));
        finish();
    }
}
