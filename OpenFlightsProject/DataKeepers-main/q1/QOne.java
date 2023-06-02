import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class QOne
{
    public static void main(String[] args) throws Exception
    {
        Configuration conf = new Configuration();
        conf.set("Country", args[2]);
        Job job = Job.getInstance(conf, "QOne");
        job.setJarByClass(QOne.class);
        job.setMapperClass(QOneMapper.class);
        job.setReducerClass(QOneReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        long start = System.currentTimeMillis();
        int result = job.waitForCompletion(true) ? 0 : 1;
        long end = System.currentTimeMillis();
        System.out.println("Elapsed time: " + (end - start));
        System.exit(result);
    }
}