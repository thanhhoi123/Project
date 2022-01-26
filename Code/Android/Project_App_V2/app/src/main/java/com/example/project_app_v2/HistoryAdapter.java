package com.example.project_app_v2;


import android.annotation.SuppressLint;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.recyclerview.widget.RecyclerView;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.PostViewHolder> {
    private List<History> mListPost;
    private Context context;
    private int p;
    private DatabaseReference mDatabase;
    public HistoryAdapter(List<History> mListPost, Context context) {
        this.mListPost = mListPost;
        this.context = context;
    }

    @NonNull
    @Override
    public PostViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.history_item,parent,false);
        return new PostViewHolder(view);
    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public void onBindViewHolder(@NonNull PostViewHolder holder, @SuppressLint("RecyclerView") final int position) {
        History post = mListPost.get(position);
        if(post == null){
            return;
        }
        holder.countDay.setText(Integer.parseInt(tinhNgay(post.getDate()))==0? "Hôm nay":tinhNgay(post.getDate())+" ngày trước");
        holder.tvTime.setText(post.getTime());
        holder.tvlogo1.setText("Tỉ lệ vật phẩm loại 1: "+post.getRatelogo1()+"%");
        holder.tvlogo2.setText("Tỉ lệ vật phẩm loại 2: "+post.getRatelogo2()+"%");
        holder.countDay.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDetail(position);
            }
        });
        holder.tvTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDetail(position);
            }
        });
        holder.tvlogo1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDetail(position);
            }
        });
        holder.tvlogo2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDetail(position);
            }
        });
        holder.countDay.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                deleteData(position);
                return false;
            }
        });
        holder.tvTime.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                deleteData(position);
                return false;
            }
        });
        holder.tvlogo1.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                deleteData(position);
                return false;
            }
        });
        holder.tvlogo2.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                deleteData(position);
                return false;
            }
        });
    }
    public void deleteData(int i){
        androidx.appcompat.app.AlertDialog.Builder e = new androidx.appcompat.app.AlertDialog.Builder(context);
        e.setTitle("WARNING");
        e.setMessage("Do you want delete this data ?");
        e.setPositiveButton("Sure", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                mDatabase = FirebaseDatabase.getInstance().getReference("");
                mDatabase.child(String.valueOf(i+1)).removeValue();
                Toast.makeText(context, "Successfully deleted user", Toast.LENGTH_SHORT).show();
            }
        });
        e.setNegativeButton("Nope", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                dialog.cancel();
            }
        });
        androidx.appcompat.app.AlertDialog a = e.create();
        a.show();
    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    public void showDetail(int position){
        Intent i = new Intent(context, ImageStorage.class);
        i.putExtra("position",String.valueOf(position+1));
        context.startActivity(i);
    }
    @Override
    public int getItemCount() {
        if(mListPost!=null) return mListPost.size();
        else return 0;
    }

    public static class PostViewHolder extends RecyclerView.ViewHolder{
        public TextView countDay;
        public TextView tvTime;
        public TextView tvlogo1;
        public TextView tvlogo2;
        public PostViewHolder(@NonNull View itemView) {
            super(itemView);
            countDay = itemView.findViewById(R.id.count_day);
            tvTime = itemView.findViewById(R.id.tv_time);
            tvlogo1 = itemView.findViewById(R.id.rate1);
            tvlogo2 = itemView.findViewById(R.id.rate2);
        }
    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    public static String tinhNgay(String Date){
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy", Locale.getDefault());
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        LocalDate firstDate = LocalDate.parse(sdf.format(new Date()), formatter);
        LocalDate secondDate = LocalDate.parse(Date, formatter);
        long days = ChronoUnit.DAYS.between(secondDate, firstDate);
        return String.valueOf(days);
    }
}

