using System.IO;


namespace FolderAndFileManipulation
{
    public class FolderFileLib
    {

        public void createDirectory(string dir_path)
        {
            Directory.CreateDirectory(dir_path);
        }

        public void deleteDirectory(string dir_path)
        {
            Directory.Delete(dir_path, true);  // true == delete recursive
        }

        public string getFilesInDirectory(string dir_path)
        {
            string[] files = Directory.GetFiles(dir_path);

            string result = "";
            foreach (string file in files)
            {
                FileInfo info = new FileInfo(file);     // File Info!
                result += info.Name +
                    info.Extension +
                    info.Length +
                    info.CreationTime +
                    info.LastAccessTime +
                    info.LastWriteTime +
                    info.Directory +
                    info.DirectoryName;
            }
            return result;
        }

        public string getDirectoriesInDirectory(string dir_path)
        {
            string[] directories = Directory.GetDirectories(dir_path);

            string result = "";
            foreach (string directory in directories)
            {
                DirectoryInfo info = new DirectoryInfo(directory);     // Directory Info!
                result += info.Name +
                    info.FullName +
                    info.CreationTime +
                    info.LastAccessTime +
                    info.LastWriteTime +
                    info.Parent;
            }
            return result;
        }

        public void moveDirectory(string source_dir, string destination_dir)
        {
            Directory.Move(source_dir, destination_dir);
        }

        public void copyFile(string file_path, string destination_path)
        {
            File.Copy(file_path, destination_path);
        }

        public void deleteFile(string file_path)
        {
            File.Delete(file_path);
        }
    }
}
