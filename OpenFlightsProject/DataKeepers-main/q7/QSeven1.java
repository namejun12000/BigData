import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class QSeven1
{
    public static void main(String[] args) throws Exception
    {
        String output = "output" + "-" + 0;
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "QSeven1");
        job.setJarByClass(QSeven1.class);
        job.setMapperClass(QSevenMapper1.class);
        job.setReducerClass(QSevenReducer1.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path("routes"));
        FileOutputFormat.setOutputPath(job, new Path(output));
        job.waitForCompletion(true);
    }
}