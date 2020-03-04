package com.fyp.fyp01;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import static android.graphics.Color.GREEN;
import static android.graphics.Color.RED;

public class ocr_final extends AppCompatActivity {

    private DatabaseReference mPostReference;

    private String doc_name, Uid;
    private String TAG = "ocr_final";

    private TextView tv;
    private int exit=0;

    private TextView name,author,path,keyphrase;
    private DatabaseReference databaseReference;

    int i=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ocr_final);

        // Get post key from intent
        Intent mPostKey = getIntent();
        doc_name = mPostKey.getStringExtra("E_POST_KEY");
        Uid = mPostKey.getStringExtra("R_POST_KEY");

        if (mPostKey == null) {
            throw new IllegalArgumentException("Must pass EXTRA_POST_KEY");
        }

        name = findViewById(R.id.name);
        author = findViewById(R.id.author);
        path = findViewById(R.id.path);
        keyphrase = findViewById(R.id.keyphrase);
        tv = findViewById(R.id.process);
        tv.setText("Wait for Processing");

        databaseReference = FirebaseDatabase.getInstance().getReference().child("Details").child(doc_name);

        // Initialize Database
        mPostReference = FirebaseDatabase.getInstance().getReference()
                .child("Requests").child("Active").child(Uid);

    }
    @Override
    public void onStart() {
        super.onStart();
        // Add value event listener to the post
        // [START post_value_event_listener]
        if(mPostReference != null){
            mPostReference.addValueEventListener(new ValueEventListener() {
                @Override
                public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                    if(dataSnapshot.exists()){
                        Document ack = dataSnapshot.getValue(Document.class);
                        if(ack.getService() == 5){
                            Toast.makeText(ocr_final.this, "Accepted", Toast.LENGTH_SHORT).show();
                            exit = 1;
                            tv.setText("Accepted");
                            fetchEmp();
                            setter(ack);
                        }
                        else if(ack.getService() == 2){
                            Toast.makeText(ocr_final.this, "Rejected", Toast.LENGTH_SHORT).show();
                            exit = 1;
                            tv.setText("Rejected");
                        }
                    }
//                    Toast.makeText(Main2Activity.this, "Request acked", Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onCancelled(@NonNull DatabaseError databaseError) {

                }
            });
        }
    }

    public void fetchEmp() {
        if(databaseReference!=null){
            databaseReference.addValueEventListener(new ValueEventListener() {
                @Override
                public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                    if(dataSnapshot.exists()){
                        Document em = dataSnapshot.getValue(Document.class);
                        setter(em);
                    }
                }

                @Override
                public void onCancelled(@NonNull DatabaseError databaseError) {

                }
            });

        }
    }

    public void setter(Document em){
        name.setText(em.getDocument_name());
        path.setText(em.getDocument_path());
        author.setText(em.getAuthor());
//        keyphrase.setText(em.getKeypharses());
    }

    @Override
    public void onBackPressed() {
        if(exit==1) {
            Intent returnIntent = new Intent();
            setResult(Activity.RESULT_CANCELED, returnIntent);
            finish();
        }
        else
            Toast.makeText(this, "Wait For Response", Toast.LENGTH_SHORT).show();
    }

    public void view_ocr(View view) {
        Toast.makeText(this, "Future Build", Toast.LENGTH_SHORT).show();
    }
}
