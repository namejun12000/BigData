import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class QSeven2 {
    public static void main(String[] args) throws Exception
    {
        Configuration conf = new Configuration();
        conf.set("TargetId1", args[1]);
        conf.set("TargetId2", args[2]);
        int rounds = Integer.parseInt(args[0]);
        for (int i = 0; i < rounds; i++)
        {
            String input = "output" + "-" + i;
            String output = "output" + "-" + (i + 1);

            Job job = Job.getInstance(conf, "QSeven2");
            job.setJarByClass(QSeven2.class);
            job.setMapperClass(QSevenMapper2.class);
            job.setReducerClass(QSevenReducer2.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);
            FileInputFormat.addInputPath(job, new Path(input));
            FileOutputFormat.setOutputPath(job, new Path(output));
            job.waitForCompletion(true);
        }
    }
}
