package com.fyp.fyp01;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void ocr_engine(View view) {
        Toast.makeText(MainActivity.this, "OCR Starting", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(this, ocr_engine.class));
//        finish();
    }

    public void search_engine(View view) {
        Toast.makeText(MainActivity.this, "Search Starting", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(this, search_engine.class));
//        finish();
    }

    public void view_engine(View view) {
        Toast.makeText(MainActivity.this, "View Starting", Toast.LENGTH_SHORT).show();
        startActivity(new Intent(this, view_engine.class));
//        finish();
    }
}
