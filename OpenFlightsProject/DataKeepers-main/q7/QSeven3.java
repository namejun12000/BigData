import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class QSeven3
{
    public static void main(String[] args) throws Exception
    { // output-1 untranslated-0
        Configuration conf = new Configuration();
        conf.set("TargetId1", args[0]);
        conf.set("TargetId2", args[1]);
        Job job = Job.getInstance(conf, "QSeven3");
        job.setJarByClass(QSeven3.class);
        job.setMapperClass(QSevenMapper3.class);
        job.setReducerClass(QSevenReducer3.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path("output-1"));
        FileOutputFormat.setOutputPath(job, new Path("untranslated-0"));
        job.waitForCompletion(true);
    }
}