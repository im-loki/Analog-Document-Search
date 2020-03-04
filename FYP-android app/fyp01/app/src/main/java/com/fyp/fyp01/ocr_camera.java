package com.fyp.fyp01;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.Continuation;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class ocr_camera extends AppCompatActivity {

    private static final int PERMISSION_CODE = 1000;
    private static final int IMAGE_CAPTURE_CODE = 1001;

    Uri image_uri;

//    private TextView tv;
    private ImageView img;
    private Button req_but;
    private EditText doc_name;
    private EditText author;
    private CheckBox allow;

    private DatabaseReference mDatabase;
    private StorageReference mStorageRef;

    String u1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ocr_camera);

        mStorageRef = FirebaseStorage.getInstance().getReference();

        FirebaseDatabase database = FirebaseDatabase.getInstance();
        mDatabase = database.getReference("Requests");

        img = findViewById(R.id.ocr_camera_iv);
        req_but = findViewById(R.id.send_db);
        doc_name = findViewById(R.id.doc_name);
        author = findViewById(R.id.author);

        img.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //if os is march and up
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    if (checkSelfPermission(Manifest.permission.CAMERA) ==
                            PackageManager.PERMISSION_DENIED ||
                            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) ==
                                    PackageManager.PERMISSION_DENIED) {
                        String[] permission = {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE};
                        requestPermissions(permission, PERMISSION_CODE);
                    } else {
                        openCamera();
                    }
                } else {
                    openCamera();
                }
            }
        });

        req_but.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (doc_name.getText().toString().isEmpty() || author.getText().toString().isEmpty()) {
                    Toast.makeText(ocr_camera.this, "Enter all data", Toast.LENGTH_LONG).show();
                }
                else
                    submitPost();
            }
        });
    }

    private void openCamera() {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "NEW PICTURE");
        values.put(MediaStore.Images.Media.DESCRIPTION, "from camera");
        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);

        Intent cIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        startActivityForResult(cIntent, IMAGE_CAPTURE_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode) {
            case PERMISSION_CODE:
                if (grantResults.length > 0 && grantResults[0] ==
                        PackageManager.PERMISSION_GRANTED)
                    openCamera();
                else
                    Toast.makeText(ocr_camera.this, "Permission denied", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        if (requestCode == IMAGE_CAPTURE_CODE && resultCode == RESULT_OK) {
            img.setImageURI(image_uri);
            img.setBackground(null);
            Glide.with(getBaseContext())
                    .load(image_uri)
                    .override(250,250)
                    .centerCrop()
                    .placeholder(R.drawable.cam_placeholder)
                    .crossFade()
                    .into(img);
//            tv.setText(image_uri.toString());
        }

        if(requestCode == IMAGE_CAPTURE_CODE && resultCode == RESULT_CANCELED){
            image_uri = null;
        }

        if (requestCode == 101 && resultCode==RESULT_CANCELED){
            resetfields();
        }
    }

    private void submitPost() {
        writeNewUser("lokeshwar1201", "lokeshwar1@gmail.com");
        //writeNewUser();
    }

    private void writeNewUser(String name, String email) {
        final ProgressDialog progress = new ProgressDialog(this);
        progress.setTitle("Uploading");
        progress.setMessage("Saving Image");
        progress.setCancelable(false);

        if (image_uri != null) {
            progress.show();

            Calendar cal = Calendar.getInstance();
            final Date date=cal.getTime();
            final StorageReference ref = mStorageRef.child("images/"+date+".jpg");
            Toast.makeText(this, image_uri.toString(), Toast.LENGTH_SHORT).show();

            UploadTask uploadTask = ref.putFile(image_uri);

            Task<Uri> urlTask = uploadTask.continueWithTask(new Continuation<UploadTask.TaskSnapshot, Task<Uri>>() {
                @Override
                public Task<Uri> then(@NonNull Task<UploadTask.TaskSnapshot> task) throws Exception {
                    if (!task.isSuccessful()) {
                        throw task.getException();
                    }

                    // Continue with the task to get the download URL
                    return ref.getDownloadUrl();
                }
            }).addOnCompleteListener(new OnCompleteListener<Uri>() {
                @Override
                public void onComplete(@NonNull Task<Uri> task) {
                    if (task.isSuccessful()) {
                        Uri downloadUri = task.getResult();

                        u1 = ref.getDownloadUrl().toString();
//                        tv.setText(u1);

                        String id = mDatabase.push().getKey();
                        Document req = new Document(doc_name.getText().toString(), downloadUri.toString(), author.getText().toString(),
                                "2020");
                        mDatabase.child("Active").child(id).setValue(req);
                        progress.dismiss();
//                        Toast.makeText(MainActivity.this, "sent", Toast.LENGTH_LONG).show();

                        Intent intent = new Intent(getBaseContext(), ocr_final.class);
                        intent.putExtra("E_POST_KEY", doc_name.getText().toString());
                        intent.putExtra("R_POST_KEY", id);

                        startActivityForResult(intent,101);

                        Toast.makeText(getBaseContext(), "Wait", Toast.LENGTH_SHORT).show();
                    } else {
                        // Handle failures
                        // ...
                    }
                }
            });


            //pd.dismiss();
        }
        else
            Toast.makeText(ocr_camera.this, "Take a Picture", Toast.LENGTH_SHORT).show();
    }

    private void resetfields(){
        doc_name.setText("");
        author.setText("");
        image_uri = null;
        img.setImageResource(R.drawable.cam_placeholder);
    }

    public void takePhoto(View view) {
        Toast.makeText(this, "Moved to img", Toast.LENGTH_SHORT).show();
    }
}
