package com.fyp.fyp01;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

public class Final_view extends AppCompatActivity {

    TextView name, author, keyphrase, ocr;
    ImageView image;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_final_view);

        name = findViewById(R.id.name);
        author = findViewById(R.id.author);
        keyphrase = findViewById(R.id.keyphrase);
        ocr = findViewById(R.id.ocr);
        image = findViewById(R.id.img);

        Intent i = getIntent();
        Document document = (Document) i.getSerializableExtra("sampleObject");

        Log.i("Intent", "onCreate: " + document.getDocument_name());

        name.setText(document.getDocument_name());
        author.setText(document.getAuthor());
        keyphrase.setText(document.getKeypharses());
//        ocr.setText(document.getDocument_json());
        Picasso.get().load(document.getDocument_path()).into(image);
    }
}
